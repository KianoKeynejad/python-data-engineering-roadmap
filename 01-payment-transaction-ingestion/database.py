import pandas as pd
from sqlalchemy import create_engine


def connect_database():

    USERNAME = "postgres"
    PASSWORD = "Emilie1234$"
    HOST = "localhost"
    PORT = 5432
    DATABASE = "payment_transactions"

    # Create database connection URL
    URL = f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(URL)   # Create SQLAlchemy engine

        with engine.connect():        # Test database connection
            print("Database connection successful!")

        return engine                 # Return engine

    except Exception as e:
        print(f"Database connection failed: {e}")
        raise




def load_transactions_to_database(df, engine):
    df.to_sql(
        "transactions",
        con=engine,
        if_exists="append",
        index=False
    )