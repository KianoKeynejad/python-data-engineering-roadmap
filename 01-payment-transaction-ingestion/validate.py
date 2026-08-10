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
        "Transaction ID",
        "Transaction Date",
        "Transaction Amount"
    ]

    # DataFrame is not empty
    if df.empty:
        raise ValueError("DataFrame is empty.")

    # Required columns
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    # Transaction ID
    if df["Transaction ID"].isnull().any():
        raise ValueError("Transaction ID contains missing values.")

    if df["Transaction ID"].duplicated().any():
        raise ValueError("Transaction ID contains duplicate values.")

    # Transaction Date
    if df["Transaction Date"].isnull().any():
        raise ValueError("Transaction Date contains missing values.")

    # Transaction Amount
    if df["Transaction Amount"].isnull().any():
        raise ValueError("Transaction Amount contains missing values.")

    if not pd.api.types.is_numeric_dtype(df["Transaction Amount"]):
        raise TypeError("Transaction Amount must be numeric.")

    print("✅ Validation passed.")