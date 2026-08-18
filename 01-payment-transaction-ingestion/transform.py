import pandas as pd
import logging

def transform_transactions(df):

    # Convert Transaction Date to datetime
    df["Transaction Date"] = pd.to_datetime(
        df["Transaction Date"],
        format="%d/%m/%Y %H:%M"
    )

    # Remove leading and trailing spaces from text columns
    for column in df.columns:
        if df[column].dtype == "object":
            df[column]= df[column].str.strip()

    # Convert text columns to uppercase
    for column in df.columns:
        if df[column].dtype == "object":
            df[column] = df[column].str.upper()

    # Handle missing values
    for column in [
        "Card Country",
        "Card Application",
        "Card Application ID"
    ]:
        df[column] = df[column].fillna("UNKNOWN")

    # Create new date columns
    df["Year"] = df["Transaction Date"].dt.year
    df["Month"] = df["Transaction Date"].dt.month
    df["Day"] = df["Transaction Date"].dt.day
    df["Hour"] = df["Transaction Date"].dt.hour

    logging.info("Transaction transformation completed")
    # Return transformed DataFrame
    return df
