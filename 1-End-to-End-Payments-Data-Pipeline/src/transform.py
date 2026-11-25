
import pandas as pd
from ingest import load_transactions
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

PROJECT_DIR = Path(__file__).resolve().parents[1]


# Step 1: Standardise column names
def standardise_column_names(df):

    # Convert column names to lowercase snake_case
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-zA-Z0-9]+", "_", regex=True)
        .str.strip("_")
    )

    return df


# Step 2: Remove leading and trailing whitespace
def remove_whitespace(df):

    df = df.copy()

    string_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in string_columns:
        df[column] = df[column].str.strip()

    return df


# Step 3: Convert columns to appropriate data types
def convert_data_types(df):

    df = df.copy()

    # Convert identifiers and text-based columns to strings
    string_columns = [
        "merchant_id",
        "id",
        "terminal_id",
        "card_bin",
        "last_4",
        "stan",
        "device_message_id",
        "site_id",
        "processor_reference_id",
        "response_code"
    ]

    for column in string_columns:
        df[column] = df[column].astype("string")

    # Convert financial and numerical columns to numeric types
    numeric_columns = [
        "transaction_amount",
        "purchase",
        "surcharge",
        "cash_out",
        "tips",
        "surcharge_percentage",
        "merchant_service_fee",
        "merchant_service_fee_percentage",
        "settlement_amount"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="raise"
        )

    return df



# Step 4: Convert transaction dates to datetime
def convert_dates(df):

    df = df.copy()

    # Convert transaction_date from string to datetime
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="raise"
    )

    return df


# Step 5: Handle missing values
def handle_missing_values(df):

    df = df.copy()

    # Identify missing values in the required columns
    required_columns = [
        "id",
        "merchant_id",
        "transaction_date",
        "transaction_type",
        "card_type",
        "last_4",
        "transaction_amount",
        "purchase",
        "surcharge",
        "payment_status",
        "account_type"
    ]

    missing_rows = df[required_columns].isna().any(axis=1)

    # Log and remove records with missing required values
    if missing_rows.any():
        logger.warning(
            "Removing %s records with missing required values",
            missing_rows.sum()
        )
        df = df.loc[~missing_rows].copy()

    return df


# Step 6: Handle duplicate transactions
def handle_duplicates(df):

    df = df.copy()

    # Identify duplicate transaction IDs
    duplicate_rows = df["id"].duplicated()

    # Log and remove duplicate transactions, keeping the first
    if duplicate_rows.any():
        logger.warning(
            "Removing %s duplicate transaction IDs",
            duplicate_rows.sum()
        )
        df = df.drop_duplicates(
            subset=["id"],
            keep="first"
        )

    return df


# Step 7: Standardise payment statuses
def standardise_payment_statuses(df):

    df = df.copy()

    # Remove surrounding whitespace and convert statuses to uppercase
    df["payment_status"] = (
        df["payment_status"]
        .str.strip()
        .str.upper()
    )

    return df


# Step 8: Clean transaction amounts
def clean_transaction_amounts(df):

    df = df.copy()

    # Convert amount columns to numeric values
    amount_columns = [
        "transaction_amount",
        "purchase",
        "surcharge"
    ]

    for column in amount_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Identify records containing invalid amounts
    invalid_amounts = df[amount_columns].isna().any(axis=1)

    if invalid_amounts.any():
        logger.warning(
            "Removing %s records with invalid transaction amounts",
            invalid_amounts.sum()
        )
        df = df.loc[~invalid_amounts].copy()

    return df


# Step 9: Apply business rules
def apply_business_rules(df):

    df = df.copy()

    # Purchases must have a positive transaction amount
    invalid_purchase_amounts = (
        df["transaction_type"].str.strip().str.lower().eq("purchase")
        & (df["transaction_amount"] <= 0)
    )

    # Transaction amount should equal purchase plus surcharge
    incorrect_totals = (
        (df["transaction_amount"] - (
            df["purchase"] + df["surcharge"]
        )).abs() > 0.01
    )

    invalid_rows = invalid_purchase_amounts | incorrect_totals

    if invalid_rows.any():
        logger.warning(
            "Removing %s records that failed business rules",
            invalid_rows.sum()
        )
        df = df.loc[~invalid_rows].copy()

    return df


# Step 10: Prepare the final dataset
def prepare_final_dataset(df):

    df = df.copy()

    # Keep only the 11 required columns in the desired order
    final_columns = [
        "id",
        "merchant_id",
        "transaction_date",
        "transaction_type",
        "card_type",
        "last_4",
        "transaction_amount",
        "purchase",
        "surcharge",
        "payment_status",
        "account_type"
    ]

    df = df[final_columns].copy()

    # Reset the DataFrame index
    df = df.reset_index(drop=True)

    logger.info(
        "Final dataset prepared with %s records and %s columns",
        df.shape[0],
        df.shape[1]
    )

    return df






if __name__ == "__main__":
    df = load_transactions()

    df = standardise_column_names(df)

    df = remove_whitespace(df)

    df = convert_data_types(df)

    df = convert_dates(df)

    df = handle_missing_values(df)

    df = handle_duplicates(df)

    df = standardise_payment_statuses(df)

    df = clean_transaction_amounts(df)

    df = apply_business_rules(df)

    df = prepare_final_dataset(df)

    # Display final dataset information
    print(df.head())
    print(df.shape)
    print(df.dtypes)

# Save the Cleaned Data

    # Step 1: Define the output file path
    OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
    OUTPUT_FILE = OUTPUT_DIR / "transactions_cleaned.csv"

    # Step 2: Create the output directory if required
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 3: Save cleaned data to CSV
    df.to_csv(OUTPUT_FILE, index=False)

    logger.info("Cleaned data saved to %s", OUTPUT_FILE)

    # Step 4: Verify the output file exists
    if not OUTPUT_FILE.exists():
        raise FileNotFoundError(OUTPUT_FILE)

    logger.info("Output file successfully created")

    # Step 5: Reload the file and verify the data
    df_reloaded = pd.read_csv(
        OUTPUT_FILE,
        parse_dates=["transaction_date"],
        dtype={
            "id": "string",
            "merchant_id": "string",
            "last_4": "string",
        },
    )

    pd.testing.assert_frame_equal(
        df.reset_index(drop=True),
        df_reloaded.reset_index(drop=True),
        check_dtype=False,
    )

    logger.info("Reloaded data successfully verified")

    # Step 6: Log the cleaning results
    logger.info(
        "Phase 6 completed: %s records and %s columns saved",
        df_reloaded.shape[0],
        df_reloaded.shape[1],
    )

