from consolidator import consolidate_data
from pathlib import Path
from pdf_renamer import find_best_patient_match


def main():
    consolidado = consolidate_data()

    pdfs = list(Path("data/laudos").glob("*.pdf"))

    patients = (
        consolidado["paciente_normalizado"]
        .dropna()
        .unique()
        .tolist()
    )

    for pdf in pdfs[:20]:
        result = find_best_patient_match(pdf.stem, patients)

        print(
            pdf.stem,
            "=>",
            result["patient"],
            result["score"],
            "OK" if result["approved"] else "REVISAO_MANUAL"
        )


if __name__ == "__main__":
    main()