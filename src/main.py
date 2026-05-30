from consolidator import consolidate_data


def main():
    consolidado = consolidate_data()

    print(consolidado.shape)
    print(consolidado["_merge"].value_counts())
    print(consolidado["divergencias"].value_counts())

    alertas = consolidado[
        consolidado["divergencias"] != "SEM_DIVERGENCIAS"
    ]

    print(
        alertas[
            [
                "id_cobranca",
                "paciente",
                "divergencias"
            ]
        ].head(20)
    )


if __name__ == "__main__":
    main()