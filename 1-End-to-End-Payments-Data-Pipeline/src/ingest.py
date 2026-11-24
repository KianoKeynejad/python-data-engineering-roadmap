
from pathlib import Path
import logging

import pandas as pd


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Define project paths
PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_DIR / "data" / "raw" / "transactions.csv"


def load_transactions() -> pd.DataFrame:
    """Read payment transactions from a CSV file."""

    logger.info("Starting transaction ingestion")

    # Check whether the input file exists
    if not INPUT_FILE.exists():
        logger.error("Input file not found: %s", INPUT_FILE)
        raise FileNotFoundError(INPUT_FILE)

    try:
        # Read CSV into a pandas DataFrame
        df = pd.read_csv(INPUT_FILE)

        logger.info("Successfully loaded %s records", len(df))

        return df

    except pd.errors.EmptyDataError:
        logger.exception("The input CSV file is empty")
        raise

    except pd.errors.ParserError:
        logger.exception("Unable to parse the CSV file")
        raise

    except OSError:
        logger.exception("File loading error")
        raise


if __name__ == "__main__":
    transactions = load_transactions()

    print("\nFirst 5 transactions:")
    print(transactions.head())

    print("\nDataset dimensions:")
    print(transactions.shape)
