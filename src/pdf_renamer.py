import re
import shutil
from pathlib import Path

from pypdf import PdfReader
from rapidfuzz import fuzz

from normalizer import normalize_name


MIN_PATIENT_PDF_SCORE = 95


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

            if pdf_patient:
                patient_similarity = fuzz.ratio(
                    pdf_patient,
                    record["paciente_normalizado"]
                )

                if patient_similarity >= MIN_PATIENT_PDF_SCORE:
                    return {
                        "approved": True,
                        "status": "OK_GUIA_PDF",
                        "patient": record["paciente_normalizado"],
                        "patient_score": patient_similarity,
                        "billing_id": record["id_cobranca"],
                        "procedure": record["procedimento"],
                        "procedure_score": 100,
                        "record": record
                    }

                return build_rejected_result(
                    status="GUIA_PDF_DIVERGE_PACIENTE",
                    patient=pdf_patient,
                    patient_score=patient_similarity,
                    billing_id=billing_id
                )

    return build_rejected_result(
        status="PACIENTE_NAO_ENCONTRADO_NO_PDF",
        billing_id=billing_id
    )


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
