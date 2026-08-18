# Payment Transaction Ingestion

## Project Overview

A Python data engineering project that ingests payment transaction data from a CSV file, explores and validates the data, cleans and transforms it, saves the processed data, and loads it into PostgreSQL.

## Project Objectives

- Read payment transaction data from CSV
- Explore and inspect the dataset
- Validate transaction data
- Clean and transform the data
- Save processed transaction data
- Connect Python to PostgreSQL using SQLAlchemy
- Load transactions into PostgreSQL
- Add application logging
- Build a reusable Python data pipeline

## Project Structure

```text
01-payment-transaction-ingestion/
├── main.py
├── ingest.py
├── explore.py
├── validate.py
├── transform.py
├── database.py
├── logging_config.py
├── requirements.txt
├── .env
├── .gitignore
├── data/
│   ├── raw/
│   └── processed/
├── logs/
└── tests/
```

## Technologies Used

- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- psycopg2
- python-dotenv
- Python logging
- pathlib
- Git / GitHub

## Data Pipeline

```text
CSV
 ↓
Load
 ↓
Explore
 ↓
Validate
 ↓
Transform
 ↓
Save processed CSV
 ↓
Connect to PostgreSQL
 ↓
Load into PostgreSQL
```

## Validation

The pipeline validates that:

- The DataFrame is not empty
- Required columns exist
- Transaction IDs contain no duplicates
- Transaction IDs contain no missing values
- Transaction dates contain no missing values
- Transaction amounts contain no missing values
- Transaction amounts are numeric

## Transformation

The pipeline:

- Converts Transaction Date to datetime
- Removes leading and trailing spaces
- Converts text values to uppercase
- Handles selected missing values using `UNKNOWN`
- Creates Year, Month, Day, and Hour columns
- Saves the cleaned data to the processed data folder

## PostgreSQL Database

The project connects to PostgreSQL using SQLAlchemy and the `psycopg2` driver.

The transformed transactions are loaded into the `payment_transactions` database and the `transactions` table.

Database credentials are stored in environment variables and are not committed to GitHub.

## Logging

The project uses Python's logging module to record important pipeline events, including:

- Program start and completion
- File loading and saving
- Validation
- Transformation
- Database connection
- PostgreSQL data loading
- Errors

Log files are stored in:

```text
logs/
```

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file containing the PostgreSQL connection details.

### 3. Run the pipeline

```bash
python main.py
```

## Environment Variables

The `.env` file should contain the PostgreSQL configuration required by the application.

Do not commit `.env` or database credentials to GitHub.

## Future Improvements

- Add automated tests
- Improve error handling
- Add database querying and analytics
- Add more robust duplicate handling
- Improve project configuration
- Add production-ready database schema management
