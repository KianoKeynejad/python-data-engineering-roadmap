"""
| File          | Purpose                   | Represents                                            |
| ------------- | ------------------------- | ----------------------------------------------------- |
| `database.py` | Database connection layer | **How the application connects to PostgreSQL**        |
| `models.py`   | Database layer            | **What the database table looks like**                |
| `schemas.py`  | API layer                 | **What data the API accepts/returns**                 |
| `services.py` | Business logic layer      | **What the application does with the data**           |
| `main.py`     | API/route layer           | **How the API receives requests and sends responses** |
"""

from fastapi import FastAPI, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import get_merchants
from app.services import get_merchant
from app.schemas import MerchantResponse

app = FastAPI()


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