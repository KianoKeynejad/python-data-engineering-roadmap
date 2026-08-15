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
        # Create SQLAlchemy engine
        engine = create_engine(URL)

        # Test database connection
        with engine.connect():
            print("Database connection successful!")

        # Return engine
        return engine

    except Exception as e:
        print(f"Database connection failed: {e}")
        raise