import pandas as pd

EXCEL_PATH = "data/cobrancas_internas.xlsx"
CSV_PATH = "data/cobrancas_convenio.csv"

from normalizer import (
    normalize_name,
    normalize_currency,
    normalize_date
)

def load_files():
    excel_df = pd.read_excel(EXCEL_PATH)
    csv_df = pd.read_csv(CSV_PATH, sep=";")

    return excel_df, csv_df


def consolidate_data():
    excel_df, csv_df = load_files()

    excel_df["paciente_normalizado"] = (
        excel_df["paciente"]
        .apply(normalize_name)
    )

    csv_df["beneficiario_normalizado"] = (
        csv_df["nome_beneficiario"]
        .apply(normalize_name)
    )

    excel_df["valor_normalizado"] = (
        excel_df["valor"]
        .apply(normalize_currency)
    )

    csv_df["vl_liquido_normalizado"] = (
        csv_df["vl_liquido"]
        .apply(normalize_currency)
    )

    consolidado = excel_df.merge(
        csv_df,
        left_on="id_cobranca",
        right_on="num_guia",
        how="outer",
        indicator=True
    )

    return consolidado