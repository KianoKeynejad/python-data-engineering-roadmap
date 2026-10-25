"""
| File          | Purpose                   | Represents                                            |
| ------------- | ------------------------- | ----------------------------------------------------- |
| `database.py` | Database connection layer | **How the application connects to PostgreSQL**        |
       ↓
| `models.py`   | Database layer            | **What the database table looks like**                | → What data do we have?
       ↓
| `schemas.py`  | API layer                 | **What data the API accepts/returns**                 | → What data do we expose? - schemas.py validates the request's structure and data types.
       ↓
| `services.py` | Business logic layer      | **What the application does with the data**           | → What do we do with the data?  - services.py contains the business logic, including checking whether a merchant exists in PostgreSQL.
       ↓
| `main.py`     | API/route layer           | **How the API receives requests and sends responses** | → How does the client access it?  - main.py handles the HTTP request and response.
"""

# http://127.0.0.1:8000/docs#/

from fastapi import FastAPI, Depends, Path, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.services import get_merchants, get_merchant, get_transactions, get_transaction, get_merchant_transactions, create_transaction
from app.schemas import MerchantResponse, TransactionResponse, TransactionCreate

app = FastAPI()

# Testing the application
@app.get("/")
def root():
    return {"message": "Testing is done"}

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    return {"message": "Database connection successful"}




@app.get("/merchants", response_model=list[MerchantResponse])
def get_all_merchants(db: Session = Depends(get_db)):
    merchants = get_merchants(db)
    return merchants


@app.get("/merchants/{merchant_id}", response_model=MerchantResponse)
def get_merchant_by_id(
        merchant_id: str = Path(min_length=1, max_length=50),
        db: Session = Depends(get_db)
):
    merchant = get_merchant(db, merchant_id)

    if merchant is None:
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

    return merchant



@app.get("/transactions", response_model= list[TransactionResponse])
def get_all_transactions(
        db: Session = Depends(get_db),
        payment_status: str | None = None,
        merchant_id: str | None = None,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
        limit: int = Query(default=100, ge=0, le=100),
        offset: int = Query(default=0, ge=0),
):
    transactions = get_transactions(
        db, payment_status, merchant_id, start_datetime, end_datetime, limit, offset
    )

    return transactions



@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction_by_id(
        transaction_id: str = Path(min_length=1, max_length=50),
        db: Session = Depends(get_db)
):
    transaction = get_transaction(db, transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction



@app.get("/merchants/{merchant_id}/transactions", response_model=list[TransactionResponse])
def get_merchant_all_transactions(
    merchant_id: str = Path(min_length=1, max_length=50),
    db: Session = Depends(get_db)
):
    merchant = get_merchant(db, merchant_id)
    if merchant is None:
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

    transactions = get_merchant_transactions(db, merchant_id)
    return transactions

@app.post("/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction_endpoint(
        transaction_data: TransactionCreate,
        db: Session = Depends(get_db)
):
    new_transaction = create_transaction(db, transaction_data)

    return new_transaction