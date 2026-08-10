from pathlib import Path

import pandas as pd


def load_transactions(csv_path: Path) -> pd.DataFrame:
    """
    Load payment transactions from a CSV file.

    Args:
        csv_path: Path to the transaction CSV file.

    Returns:
        A pandas DataFrame containing the transaction data.
    """
    try:
        df = pd.read_csv(csv_path)
        return df

    except FileNotFoundError:
        print(f"Transaction file not found: {csv_path}")
        raise
