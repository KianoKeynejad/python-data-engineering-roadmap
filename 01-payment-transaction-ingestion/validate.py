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
import logging


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
        raise ValueError("DataFrame is empty.")

    # Required columns
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    # Check ID has no missing values
    if df["ID"].isnull().any():
        raise ValueError("ID contains missing values.")

    # Check ID has no duplicates
    if df["ID"].duplicated().any():
        raise ValueError("ID contains duplicate values.")

    # Check Transaction Date has no missing values
    if df["Transaction Date"].isnull().any():
        raise ValueError("Transaction Date contains missing values.")

    # Check Transaction Amount has no missing values
    if df["Transaction Amount"].isnull().any():
        raise ValueError("Transaction Amount contains missing values.")

    # Check Transaction Amount is numeric
    if not pd.api.types.is_numeric_dtype(df["Transaction Amount"]):
        raise TypeError("Transaction Amount must be numeric.")

    logging.info("Transaction validation passed")