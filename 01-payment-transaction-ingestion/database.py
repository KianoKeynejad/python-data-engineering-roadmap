import os
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def connect_database():

    USERNAME = os.getenv("DB_USERNAME")
    PASSWORD = os.getenv("DB_PASSWORD")
    HOST = os.getenv("DB_HOST")
    PORT = os.getenv("DB_PORT")
    DATABASE = os.getenv("DB_NAME")

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
        if_exists="replace",
        index=False
    )

    logging.info("Transactions loaded into PostgreSQL")