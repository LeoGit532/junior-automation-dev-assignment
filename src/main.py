from pathlib import Path

from consolidator import consolidate_data
from pdf_renamer import find_best_billing_match, rename_report
from report_generator import generate_report

def main():
    consolidado = consolidate_data()
    
  
    pdfs = list(Path("data/laudos").glob("*.pdf"))

    total = len(pdfs)
    renomeados = 0
    revisao_manual = 0
    ja_existia = 0
    motivos = {}

    for pdf in pdfs:
        result = find_best_billing_match(pdf, consolidado)

        if not result["approved"]:
            revisao_manual += 1
            motivos[result["status"]] = motivos.get(result["status"], 0) + 1
            print(f"REVISAO_MANUAL -> {pdf.name} | {result['status']}")
            continue

        success, message = rename_report(pdf, result["record"])

        if success:
            renomeados += 1
        elif message == "ARQUIVO_JA_EXISTE":
            ja_existia += 1

        print(f"{pdf.name} => {message}")

    print("\n=== RESUMO DOS LAUDOS ===")
    print(f"Total de PDFs: {total}")
    print(f"Renomeados com sucesso: {renomeados}")
    print(f"Já existiam: {ja_existia}")
    print(f"Revisão manual: {revisao_manual}")

    print("\nMotivos de revisão:")
    for status, quantidade in motivos.items():
        print(f"{status}: {quantidade}")
        
        print("\n=== VALIDAÇÃO DOS PDFS RENOMEADOS ===")

    from pdf_renamer import extract_billing_id_from_pdf, extract_patient_from_pdf

    erros_validacao = 0

    for pdf in Path("output/laudos_renomeados").glob("*.pdf"):
        filename_parts = pdf.stem.split("-")

        if len(filename_parts) < 4:
            print(f"NOME_INVALIDO -> {pdf.name}")
            erros_validacao += 1
            continue

        file_patient = filename_parts[1]
        file_billing_id = filename_parts[2]

        pdf_patient = extract_patient_from_pdf(pdf)
        pdf_billing_id = extract_billing_id_from_pdf(pdf)

        if pdf_billing_id and file_billing_id != pdf_billing_id:
            print(f"ERRO_GUIA -> {pdf.name} | PDF: {pdf_billing_id}")
            erros_validacao += 1

        if pdf_patient and file_patient != pdf_patient.replace(" ", ""):
            print(f"ERRO_PACIENTE -> {pdf.name} | PDF: {pdf_patient}")
            erros_validacao += 1

    print(f"Erros encontrados na validação: {erros_validacao}")   

    from pathlib import Path

from consolidator import consolidate_data
from pdf_renamer import find_best_billing_match, rename_report
from report_generator import generate_report

def main():
    consolidado = consolidate_data()
    
  
    pdfs = list(Path("data/laudos").glob("*.pdf"))

    total = len(pdfs)
    renomeados = 0
    revisao_manual = 0
    ja_existia = 0
    motivos = {}

    for pdf in pdfs:
        result = find_best_billing_match(pdf, consolidado)

        if not result["approved"]:
            revisao_manual += 1
            motivos[result["status"]] = motivos.get(result["status"], 0) + 1
            print(f"REVISAO_MANUAL -> {pdf.name} | {result['status']}")
            continue

        success, message = rename_report(pdf, result["record"])

        if success:
            renomeados += 1
        elif message == "ARQUIVO_JA_EXISTE":
            ja_existia += 1

        print(f"{pdf.name} => {message}")

    print("\n=== RESUMO DOS LAUDOS ===")
    print(f"Total de PDFs: {total}")
    print(f"Renomeados com sucesso: {renomeados}")
    print(f"Já existiam: {ja_existia}")
    print(f"Revisão manual: {revisao_manual}")

    print("\nMotivos de revisão:")
    for status, quantidade in motivos.items():
        print(f"{status}: {quantidade}")
        
    print("\n=== VALIDAÇÃO DOS PDFS RENOMEADOS ===")

    from pdf_renamer import extract_billing_id_from_pdf, extract_patient_from_pdf

    erros_validacao = 0

    for pdf in Path("output/laudos_renomeados").glob("*.pdf"):
        filename_parts = pdf.stem.split("-")

        if len(filename_parts) < 4:
            print(f"NOME_INVALIDO -> {pdf.name}")
            erros_validacao += 1
            continue

        file_patient = filename_parts[1]
        file_billing_id = filename_parts[2]

        pdf_patient = extract_patient_from_pdf(pdf)
        pdf_billing_id = extract_billing_id_from_pdf(pdf)

        if pdf_billing_id and file_billing_id != pdf_billing_id:
            print(f"ERRO_GUIA -> {pdf.name} | PDF: {pdf_billing_id}")
            erros_validacao += 1

        if pdf_patient and file_patient != pdf_patient.replace(" ", ""):
            print(f"ERRO_PACIENTE -> {pdf.name} | PDF: {pdf_patient}")
            erros_validacao += 1

    print(f"Erros encontrados na validação: {erros_validacao}")   

    pdf_summary = {
        "total": total,
        "renomeados": renomeados,
        "revisao_manual": revisao_manual
    }

    report_path = generate_report(consolidado, pdf_summary)

    print(f"\nRelatório gerado: {report_path}")


if __name__ == "__main__":
    main()