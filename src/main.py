from consolidator import load_files
from normalizer import normalize_name, normalize_currency, normalize_date


def main():
    excel_df, csv_df = load_files()

    print(normalize_name("Fernanda Costa"))
    print(normalize_name("COSTA, FERNANDA"))

    print(normalize_currency("260,00"))
    print(normalize_currency(260))

    print(normalize_date("01/11/2024"))
    print(normalize_date("2024-11-04"))


if __name__ == "__main__":
    main()