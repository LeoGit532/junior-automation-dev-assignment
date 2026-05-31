from pathlib import Path

from consolidator import consolidate_data
from email_sender import send_report_email
from pdf_renamer import (
    extract_billing_id_from_pdf,
    extract_patient_from_pdf,
    find_best_billing_match,
    rename_report,
)
from report_generator import generate_report


PDF_INPUT_DIR = Path("data/laudos")
RENAMED_PDF_DIR = Path("output/laudos_renomeados")


def process_reports(consolidado):
    pdfs = list(PDF_INPUT_DIR.glob("*.pdf"))

    summary = {
        "total": len(pdfs),
        "renomeados": 0,
        "revisao_manual": 0,
    }
    already_exists = 0
    review_reasons = {}

    for pdf in pdfs:
        result = find_best_billing_match(pdf, consolidado)

        if not result["approved"]:
            summary["revisao_manual"] += 1
            status = result["status"]
            review_reasons[status] = review_reasons.get(status, 0) + 1
            print(f"REVISAO_MANUAL -> {pdf.name} | {status}")
            continue

        success, message = rename_report(pdf, result["record"])

        if success:
            summary["renomeados"] += 1
        elif message == "ARQUIVO_JA_EXISTE":
            already_exists += 1

        print(f"{pdf.name} => {message}")

    return summary, already_exists, review_reasons


def print_report_summary(summary, already_exists, review_reasons):
    print("\n=== RESUMO DOS LAUDOS ===")
    print(f"Total de PDFs: {summary['total']}")
    print(f"Renomeados com sucesso: {summary['renomeados']}")
    print(f"Ja existiam: {already_exists}")
    print(f"Revisao manual: {summary['revisao_manual']}")

    print("\nMotivos de revisao:")
    for status, quantity in review_reasons.items():
        print(f"{status}: {quantity}")


def validate_renamed_reports():
    print("\n=== VALIDACAO DOS PDFS RENOMEADOS ===")

    validation_errors = 0

    for pdf in RENAMED_PDF_DIR.glob("*.pdf"):
        filename_parts = pdf.stem.split("-")

        if len(filename_parts) < 4:
            print(f"NOME_INVALIDO -> {pdf.name}")
            validation_errors += 1
            continue

        file_patient = filename_parts[1]
        file_billing_id = filename_parts[2]

        pdf_patient = extract_patient_from_pdf(pdf)
        pdf_billing_id = extract_billing_id_from_pdf(pdf)

        if pdf_billing_id and file_billing_id != pdf_billing_id:
            print(f"ERRO_GUIA -> {pdf.name} | PDF: {pdf_billing_id}")
            validation_errors += 1

        if pdf_patient and file_patient != pdf_patient.replace(" ", ""):
            print(f"ERRO_PACIENTE -> {pdf.name} | PDF: {pdf_patient}")
            validation_errors += 1

    print(f"Erros encontrados na validacao: {validation_errors}")
    return validation_errors


def main():
    consolidado = consolidate_data()

    pdf_summary, already_exists, review_reasons = process_reports(consolidado)

    print_report_summary(
        pdf_summary,
        already_exists,
        review_reasons,
    )
    validate_renamed_reports()

    report_path = generate_report(consolidado, pdf_summary)
    print(f"\nRelatorio gerado: {report_path}")

    send_report_email(report_path, pdf_summary)


if __name__ == "__main__":
    main()
