def load_transactions_to_database(df, engine):
    df.to_sql(
        name="transactions",
        con=engine,
        if_exists="append",
        index=False
    )

try:
    engine = create_engine(URL)
    with engine.connect():
        print("Database connection successful!")
    return engine
except Exception as e:
    print(e)
    raise

