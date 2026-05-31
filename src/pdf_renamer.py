import re
import shutil
from pathlib import Path

from pypdf import PdfReader
from rapidfuzz import process, fuzz

from normalizer import normalize_name


MIN_PATIENT_SCORE = 80
MIN_PROCEDURE_SCORE = 65
MIN_SCORE_GAP = 10

PROCEDURE_ALIASES = {
    "ECO": "ECOCARDIOGRAMA",
    "ELE": "ELETROCARDIOGRAMA",
    "END": "ENDOSCOPIA DIGESTIVA",
    "RES": "RESSONANCIA MAGNETICA",
    "TOM": "TOMOGRAFIA COMPUTADORIZADA",
    "ULT": "ULTRASSOM ABDOMINAL",
    "ESP": "ESPIROMETRIA",
    "RAI": "RAIO X TORAX",
    "EXA": "EXAME DE SANGUE COMPLETO",
}


def extract_pdf_text(pdf_path):
    reader = PdfReader(str(pdf_path))
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def extract_patient_from_pdf(pdf_path):
    try:
        text = extract_pdf_text(pdf_path)
    except Exception:
        return None

    match = re.search(r"Paciente:\s*(.+)", text)

    if match:
        return normalize_name(match.group(1).strip())

    return None


def extract_billing_id_from_pdf(pdf_path):
    try:
        text = extract_pdf_text(pdf_path)
    except Exception:
        return None

    match = re.search(r"COB\d+", text)

    if match:
        return match.group(0)

    return None


def normalize_pdf_name(pdf_name):
    cleaned = pdf_name.lower()

    cleaned = cleaned.replace("_", " ")
    cleaned = cleaned.replace("-", " ")

    cleaned = re.sub(r"\bnov\s?24\b", " ", cleaned)
    cleaned = re.sub(r"\b\d{1,2}\s\d{1,2}\b", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    normalized = normalize_name(cleaned)

    words = normalized.split()
    expanded_words = [
        PROCEDURE_ALIASES.get(word, word)
        for word in words
    ]

    return " ".join(expanded_words)


def find_best_patient_match(pdf_name, patient_names):
    normalized_pdf_name = normalize_pdf_name(pdf_name)

    matches = process.extract(
        normalized_pdf_name,
        patient_names,
        scorer=fuzz.partial_ratio,
        limit=2
    )

    if not matches:
        return {
            "patient": None,
            "score": 0,
            "second_score": 0,
            "score_gap": 0,
            "status": "SEM_MATCH",
            "approved": False
        }

    best_patient, best_score, _ = matches[0]
    second_score = matches[1][1] if len(matches) > 1 else 0
    score_gap = best_score - second_score

    if best_score < MIN_PATIENT_SCORE:
        status = "BAIXA_CONFIANCA"
        approved = False
    elif best_score < 100 and score_gap < MIN_SCORE_GAP:
        status = "AMBIGUO"
        approved = False
    else:
        status = "OK"
        approved = True

    return {
        "patient": best_patient,
        "score": best_score,
        "second_score": second_score,
        "score_gap": score_gap,
        "status": status,
        "approved": approved
    }


def find_record_by_billing_id(billing_id, consolidado):
    match = consolidado[
        consolidado["id_cobranca"].eq(billing_id)
        | consolidado["num_guia"].eq(billing_id)
    ]

    if match.empty:
        return None

    return match.iloc[0]


def build_rejected_result(status, patient=None, patient_score=0, billing_id=None):
    return {
        "approved": False,
        "status": status,
        "patient": patient,
        "patient_score": patient_score,
        "billing_id": billing_id,
        "procedure": None,
        "procedure_score": 0,
        "record": None
    }


def find_best_billing_match(pdf_path, consolidado):
    billing_id = extract_billing_id_from_pdf(pdf_path)

    if billing_id:
        record = find_record_by_billing_id(
            billing_id,
            consolidado
        )

        if record is not None:
            pdf_patient = extract_patient_from_pdf(
                pdf_path
            )

            if (
                pdf_patient
                and pdf_patient == record["paciente_normalizado"]
            ):
                return {
                    "approved": True,
                    "status": "OK_GUIA_PDF",
                    "patient": record["paciente_normalizado"],
                    "patient_score": 100,
                    "billing_id": record["id_cobranca"],
                    "procedure": record["procedimento"],
                    "procedure_score": 100,
                    "record": record
                }
                
            return build_rejected_result(
                status="GUIA_PDF_DIVERGE_PACIENTE",
                patient=pdf_patient,
                billing_id=billing_id
            )
    pdf_name = Path(pdf_path).stem

    patients = (
        consolidado["paciente_normalizado"]
        .dropna()
        .unique()
        .tolist()
    )

    patient_result = find_best_patient_match(
        pdf_name,
        patients
    )

    if not patient_result["approved"]:
        return build_rejected_result(
            status=patient_result["status"],
            patient=patient_result["patient"],
            patient_score=patient_result["score"]
        )

    patient_records = consolidado[
        consolidado["paciente_normalizado"]
        == patient_result["patient"]
    ].copy()

    procedure_choices = {
        normalize_name(row["procedimento"]): index
        for index, row in patient_records.iterrows()
    }

    normalized_pdf_name = normalize_pdf_name(
        pdf_name
    )

    procedure_match = process.extractOne(
        normalized_pdf_name,
        list(procedure_choices.keys()),
        scorer=fuzz.token_set_ratio
    )

    if procedure_match is None:
        return build_rejected_result(
            status="SEM_PROCEDIMENTO",
            patient=patient_result["patient"],
            patient_score=patient_result["score"]
        )

    procedure_name, procedure_score, _ = procedure_match

    record_index = procedure_choices[
        procedure_name
    ]

    record = consolidado.loc[
        record_index
    ]

    approved = (
        procedure_score
        >= MIN_PROCEDURE_SCORE
    )

    if not approved:
        return build_rejected_result(
            status="PROCEDIMENTO_BAIXA_CONFIANCA",
            patient=patient_result["patient"],
            patient_score=patient_result["score"],
            billing_id=record["id_cobranca"]
        )

    return {
        "approved": True,
        "status": "OK_SIMILARIDADE",
        "patient": patient_result["patient"],
        "patient_score": patient_result["score"],
        "billing_id": record["id_cobranca"],
        "procedure": record["procedimento"],
        "procedure_score": procedure_score,
        "record": record
    }


def generate_pdf_filename(record):
    cpf = str(record["cpf_beneficiario"]).replace(".", "").replace("-", "")

    patient = record["paciente_normalizado"].replace(" ", "")
    billing_id = record["id_cobranca"]

    date_str = str(record["data_atendimento"])
    month = date_str[3:5]
    year = date_str[6:10]

    return f"{cpf}-{patient}-{billing_id}-{month}{year}.pdf"


def rename_report(pdf_path, record):
    output_dir = Path("output/laudos_renomeados")
    output_dir.mkdir(parents=True, exist_ok=True)

    new_filename = generate_pdf_filename(record)
    destination = output_dir / new_filename

    if destination.exists():
        return False, "ARQUIVO_JA_EXISTE"

    shutil.copy2(pdf_path, destination)

    return True, new_filename