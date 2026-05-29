from consolidator import load_files


def main():
    excel_df, csv_df = load_files()

    print("=== EXCEL ===")
    print(excel_df.columns.tolist())
    print(excel_df.head())

    print("\n=== CSV ===")
    print(csv_df.columns.tolist())
    print(csv_df.head())


if __name__ == "__main__":
    main()