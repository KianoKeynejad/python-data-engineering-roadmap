import pandas as pd


def explore_transactions(df: pd.DataFrame) -> None:
    """
    Explore the transaction dataset.
    """

    print("\n===== FIRST 5 ROWS =====")
    print(df.head())

    print("\n===== DATAFRAME INFO =====")
    df.info()

    print("\n===== SUMMARY STATISTICS =====")
    print(df.describe(include="all"))

    print("\n===== MISSING VALUES =====")
    print(df.isnull().sum())

    print("\n===== DATA TYPES =====")
    print(df.dtypes)

    print("\n===== SHAPE =====")
    print(df.shape)

    print("\n===== DUPLICATE ROWS =====")
    print(df.duplicated().sum())