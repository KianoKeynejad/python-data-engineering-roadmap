from sqlalchemy import create_engine
import logging


def connect_database():

    USERNAME = "postgres"
    PASSWORD = "Emilie1234$"
    HOST = "localhost"
    PORT = 5432
    DATABASE = "payment_transactions"

    # Create database connection URL
    URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(URL)

        # Test database connection
        with engine.connect():
            logging.info("Database connection successful!")

        return engine

    except Exception:
        logging.error("Database connection failed", exc_info=True)
        raise


def load_transactions_to_database(df, engine):

    df.to_sql(
        "transactions",
        con=engine,
        if_exists="append",
        index=False
    )

    logging.info("Transactions loaded into PostgreSQL")