from consolidator import consolidate_data


def main():
    consolidado = consolidate_data()

    print(consolidado.shape)
    print(consolidado.head())
    print(consolidado["_merge"].value_counts())


if __name__ == "__main__":
    main()