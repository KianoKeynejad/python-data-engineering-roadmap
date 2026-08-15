"""
Our first validation rules:

✓ DataFrame is not empty

✓ Required columns exist
    - ID
    - Transaction Date
    - Transaction Amount

✓ ID has no duplicates

✓ ID has no missing values

✓ Transaction Date has no missing values

✓ Transaction Amount has no missing values
"""
import pandas as pd


def validate_transactions(df: pd.DataFrame) -> None:
    """
    Validate the transaction dataset.
    """

    required_columns = [
        "ID",
        "Transaction Date",
        "Transaction Amount"
    ]

    # DataFrame is not empty
    if df.empty:
        raise ValueError("Dataframe is empty.")

    # Required columns
    for col in required_columns:
        if col not in df.columns():
            raise ValueError(f"column {col} is not in dataframe.")

    # Check ID has no missing values
    if df["ID"].isnull().any():
        raise ValueError("ID is null")

    # Check ID has no duplicates
    if df["ID"].duplicated().any():
        raise ValueError("ID is duplicated")

    # Check Transaction Date has no missing values
    if df["Transaction Date"].isnull().any():
        raise ValueError("Transaction Date is null")

    # Check Transaction Amount has no missing values
    if df["Transaction Amount"].isnull().any():
        raise ValueError("Transaction Amount is null")

    # Check Transaction Amount is numeric
    if not pd.api.type.is_numeric_dtype(df["Transaction Amount"]):
        raise ValueError("Transaction Amount is not numeric")

    print("✅ Validation passed.")