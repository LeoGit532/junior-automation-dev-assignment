import pandas as pd

from normalizer import (
    normalize_name,
    normalize_currency,
    normalize_ans
)

EXCEL_PATH = "data/cobrancas_internas.xlsx"
CSV_PATH = "data/cobrancas_convenio.csv"


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

    consolidado["divergencias"] = consolidado.apply(
        detect_divergences,
        axis=1
    )

    return consolidado


def detect_divergences(row):
    divergencias = []

    if row["_merge"] == "right_only":
        divergencias.append("FONTE_UNICA_CSV")

    if row["_merge"] == "left_only":
        divergencias.append("FONTE_UNICA_EXCEL")

    if row["_merge"] == "both":
        if (
            abs(
                row["valor_normalizado"]
                - row["vl_liquido_normalizado"]
            )
            > 0.01
        ):
            divergencias.append("DIVERGENCIA_VALOR")

        if (
            row["paciente_normalizado"]
            != row["beneficiario_normalizado"]
        ):
            divergencias.append("DIVERGENCIA_NOME")

        if (
            normalize_ans(row["registro_ans"])
            != normalize_ans(row["ans"])
        ):
            divergencias.append("DIVERGENCIA_CONVENIO")

    if not divergencias:
        return "SEM_DIVERGENCIAS"

    return ";".join(divergencias)