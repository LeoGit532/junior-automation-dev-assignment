import pandas as pd

EXCEL_PATH = "data/cobrancas_internas.xlsx"
CSV_PATH = "data/cobrancas_convenio.csv"


def load_files():
    excel_df = pd.read_excel(EXCEL_PATH)
    csv_df = pd.read_csv(CSV_PATH, sep=";")

    return excel_df, csv_df