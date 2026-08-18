from pathlib import Path

import logging
import pandas as pd


def load_transactions(csv_path: Path) -> pd.DataFrame:
    """
    Load payment transactions from a CSV file.

    Args:
        csv_path: Path to the transaction CSV file.

    Returns:
        A pandas DataFrame containing the transaction data.
    """

    logging.info(f"Loading transactions from {csv_path}")

    try:
        df = pd.read_csv(csv_path)

        logging.info(f"Transactions loaded successfully from {csv_path}")

        return df

    except FileNotFoundError:
        logging.error(f"Transaction file not found: {csv_path}")
        raise


def save_transactions(df: pd.DataFrame, csv_path: Path):
    """
    Save transactions to a CSV file.

    Args:
        df: DataFrame containing transaction data.
        csv_path: Path to save the transaction CSV file.
    """

    df.to_csv(csv_path, index=False)

    logging.info(f"Transactions saved to {csv_path}")