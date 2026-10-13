"""
| File          | Purpose                   | Represents                                            |
| ------------- | ------------------------- | ----------------------------------------------------- |
| `database.py` | Database connection layer | **How the application connects to PostgreSQL**        |
       ↓
| `models.py`   | Database layer            | **What the database table looks like**                | → What data do we have?
       ↓
| `schemas.py`  | API layer                 | **What data the API accepts/returns**                 | → What data do we expose?
       ↓
| `services.py` | Business logic layer      | **What the application does with the data**           | → What do we do with the data?
       ↓
| `main.py`     | API/route layer           | **How the API receives requests and sends responses** | → How does the client access it?
"""

# http://127.0.0.1:8000/docs#/

from fastapi import FastAPI, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import get_merchants, get_merchant, get_transactions, get_transaction, get_merchant_transactions
from app.schemas import MerchantResponse, TransactionResponse

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
def get_all_transactions(db: Session = Depends(get_db)):
    transactions = get_transactions(db)
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

