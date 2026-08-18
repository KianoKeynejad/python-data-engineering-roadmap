from pathlib import Path

from ingest import load_transactions, save_transactions
from explore import explore_transactions
from validate import validate_transactions
from transform import transform_transactions
from database import connect_database, load_transactions_to_database
from logging_config import setup_logging



def main():
    logger = setup_logging()
    logger.info("Program started")

    csv_path = Path("data/raw/transactions.csv")

    df = load_transactions(csv_path)

    explore_transactions(df)

    validate_transactions(df)
    logger.info("Validation passed")

    df = transform_transactions(df)

    processed_path = Path("data/processed/transactions_clean.csv")

    save_transactions(df, processed_path)

    print(
        df[
            [
                "Transaction Date",
                "Year",
                "Month",
                "Day",
                "Hour",
            ]
        ].head()
    )

    engine = connect_database()

    load_transactions_to_database(df, engine)

    logger.info("Program completed successfully")


if __name__ == "__main__":
    main()

"""
This is the standard Python entry point.

It means:

"If this file is being run directly, execute the main() function."

This allows main.py to be run as the application, while also allowing its functions to be imported into other modules without automatically executing the pipeline.
"""