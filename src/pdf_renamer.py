from rapidfuzz import process, fuzz
from normalizer import normalize_name

MIN_MATCH_SCORE = 80


def normalize_pdf_name(pdf_name):
    cleaned = pdf_name.replace("_", " ").replace("-", " ")
    return normalize_name(cleaned)


def find_best_patient_match(pdf_name, patient_names):
    normalized_pdf_name = normalize_pdf_name(pdf_name)

    match = process.extractOne(
        normalized_pdf_name,
        patient_names,
        scorer=fuzz.partial_ratio
    )

    if match is None:
        return {
            "patient": None,
            "score": 0,
            "approved": False
        }

    patient, score, index = match

    return {
        "patient": patient,
        "score": score,
        "approved": score >= MIN_MATCH_SCORE
    }