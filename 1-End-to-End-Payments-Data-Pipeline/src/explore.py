
from ingest import load_transactions
import pandas as pd


# Load transaction data
df = load_transactions()


# 1. Display the first rows
print("\n--- First 5 Rows ---")
print(df.head())


# 2. Check number of rows and columns
print("\n--- Dataset Dimensions ---")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# 3. Inspect column names
print("\n--- Column Names ---")
print(df.columns.tolist())


# 4. Check data types
print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- DataFrame Information ---")
df.info()


# 5. Review summary statistics
print("\n--- Summary Statistics ---")
print(df.describe(include="all"))


# 6. Identify missing values
print("\n--- Missing Values ---")
print(df.isnull().sum())


# 7. Identify duplicate records
print("\n--- Duplicate Records ---")
print(df.duplicated().sum())


# 8. Inspect payment statuses
print("\n--- Payment Statuses ---")
if "payment_status" in df.columns:
    print(df["payment_status"].value_counts(dropna=False))
else:
    print("payment_status column not found")


# 9. Inspect merchant IDs
print("\n--- Merchant IDs ---")
if "merchant_id" in df.columns:
    print(df["merchant_id"].value_counts(dropna=False))
else:
    print("merchant_id column not found")


# 10. Inspect transaction dates and amounts
print("\n--- Transaction Dates ---")

date_columns = [
    col for col in df.columns
    if "date" in col.lower() or "time" in col.lower()
]

for column in date_columns:
    print(f"\n{column}")
    print(df[column].describe())


print("\n--- Transaction Amounts ---")

amount_columns = [
    col for col in df.columns
    if "amount" in col.lower()
]

for column in amount_columns:
    print(f"\n{column}")
    print(df[column].describe())
