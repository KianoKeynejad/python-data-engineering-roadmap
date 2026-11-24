
import logging
from pathlib import Path

import pandas as pd

from ingest import load_transactions


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]

MERCHANTS_FILE = PROJECT_DIR / "data" / "raw" / "merchants.csv"

LOG_FILE = PROJECT_DIR / "logs" / "validation.log"

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 1. Validate required columns
# --------------------------------------------------

def validate_required_columns(df):

    required_columns = [
        "ID",
        "Merchant ID",
        "Transaction Date",
        "Transaction Type",
        "Card Type",
        "Last 4",
        "Transaction Amount",
        "Purchase",
        "Surcharge",
        "Payment Status",
        "Account Type"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        logger.error("Missing required columns: %s", missing_columns)
        return False

    logger.info("All required columns are present")
    return True


# --------------------------------------------------
# 2. Validate transaction IDs
# --------------------------------------------------

def validate_transaction_ids(df):

    ids = df["ID"].astype("string").str.strip()

    invalid_ids = ids.isna() | ids.eq("")

    if invalid_ids.any():
        logger.error(
            "Found %s missing or blank transaction IDs",
            invalid_ids.sum()
        )
        return False

    logger.info("Transaction IDs are valid")
    return True


# --------------------------------------------------
# 3. Validate merchant IDs
# --------------------------------------------------

def validate_merchant_ids(df):

    merchant_ids = df["Merchant ID"].astype("string").str.strip()

    invalid_ids = merchant_ids.isna() | merchant_ids.eq("")

    if invalid_ids.any():
        logger.error(
            "Found %s missing or blank merchant IDs",
            invalid_ids.sum()
        )
        return False

    logger.info("Merchant IDs are valid")
    return True


# --------------------------------------------------
# 4. Validate transaction amounts
# --------------------------------------------------

def validate_transaction_amounts(df):

    amounts = pd.to_numeric(
        df["Transaction Amount"],
        errors="coerce"
    )

    invalid_amounts = amounts.isna() | (amounts <= 0)

    if invalid_amounts.any():
        logger.error(
            "Found %s invalid transaction amounts",
            invalid_amounts.sum()
        )
        return False

    logger.info("Transaction amounts are valid")
    return True


# --------------------------------------------------
# 5. Validate payment statuses
# --------------------------------------------------

def validate_payment_statuses(df):

    statuses = df["Payment Status"].astype("string").str.strip()

    invalid_statuses = statuses.isna() | statuses.eq("")

    if invalid_statuses.any():
        logger.error(
            "Found %s missing or blank payment statuses",
            invalid_statuses.sum()
        )
        return False

    logger.info(
        "Payment statuses are present. Observed statuses: %s",
        statuses.unique().tolist()
    )
    return True


# --------------------------------------------------
# 6. Validate transaction dates
# --------------------------------------------------

def validate_transaction_dates(df):

    dates = pd.to_datetime(
        df["Transaction Date"],
        format="%d/%m/%Y %H:%M",
        errors="coerce"
    )

    invalid_dates = dates.isna()

    if invalid_dates.any():
        logger.error(
            "Found %s invalid transaction dates",
            invalid_dates.sum()
        )
        return False

    logger.info("Transaction dates are valid")
    return True


# --------------------------------------------------
# 7. Check for missing values
# --------------------------------------------------

def validate_missing_values(df):

    required_columns = [
        "ID",
        "Merchant ID",
        "Transaction Date",
        "Transaction Type",
        "Card Type",
        "Last 4",
        "Transaction Amount",
        "Purchase",
        "Surcharge",
        "Payment Status",
        "Account Type"
    ]

    missing_values = df[required_columns].isnull().sum()

    missing_values = missing_values[missing_values > 0]

    if not missing_values.empty:
        logger.error(
            "Missing values found: %s",
            missing_values.to_dict()
        )
        return False

    logger.info("No missing values in required columns")
    return True


# --------------------------------------------------
# 8. Check for duplicate transactions
# --------------------------------------------------

def validate_duplicates(df):

    duplicate_ids = df["ID"].duplicated().sum()

    duplicate_rows = df.duplicated().sum()

    if duplicate_ids > 0 or duplicate_rows > 0:
        logger.error(
            "Found %s duplicate transaction IDs and %s identical rows",
            duplicate_ids,
            duplicate_rows
        )
        return False

    logger.info("No duplicate transactions found")
    return True


# --------------------------------------------------
# 9. Validate merchant references
# --------------------------------------------------

def validate_merchant_references(df, merchants_df):

    transaction_merchants = (
        df["Merchant ID"].astype("string").str.strip()
    )

    merchant_records = (
        merchants_df["Merchant ID"].astype("string").str.strip()
    )

    known_merchants = set(merchant_records.dropna())

    unknown_merchants = (
        ~transaction_merchants.isin(known_merchants)
    )

    if unknown_merchants.any():

        missing_ids = (
            transaction_merchants[unknown_merchants]
            .dropna()
            .unique()
            .tolist()
        )

        logger.error(
            "Found %s transactions with unknown merchant IDs: %s",
            unknown_merchants.sum(),
            missing_ids[:10]
        )
        return False

    logger.info("All transaction merchant references are valid")
    return True


# --------------------------------------------------
# 10. Run all validations
# --------------------------------------------------

def validate_transactions(df, merchants_df):

    validation_results = {
        "Required columns": validate_required_columns(df),
        "Transaction IDs": validate_transaction_ids(df),
        "Merchant IDs": validate_merchant_ids(df),
        "Transaction amounts": validate_transaction_amounts(df),
        "Payment statuses": validate_payment_statuses(df),
        "Transaction dates": validate_transaction_dates(df),
        "Missing values": validate_missing_values(df),
        "Duplicate transactions": validate_duplicates(df),
        "Merchant references": validate_merchant_references(
            df, merchants_df
        )
    }

    print("\n--- Validation Results ---")

    for validation, result in validation_results.items():
        print(f"{validation}: {'PASSED' if result else 'FAILED'}")

    overall_result = all(validation_results.values())

    if overall_result:
        logger.info("All data validations passed")
    else:
        logger.error("One or more data validations failed")

    return overall_result


# --------------------------------------------------
# Main execution
# --------------------------------------------------

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

    df = load_transactions()

    if not MERCHANTS_FILE.exists():
        raise FileNotFoundError(
            f"Merchant file not found: {MERCHANTS_FILE}"
        )

    merchants_df = pd.read_csv(
        MERCHANTS_FILE,
        dtype={"Merchant ID": "string"}
    )

    if validate_required_columns(df):
        result = validate_transactions(df, merchants_df)
        print("\nOverall validation passed:", result)
    else:
        print("\nOverall validation passed: False")
