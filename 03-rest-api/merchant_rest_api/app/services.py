# | `services.py` | Business logic layer      | **What the application does with the data**           |

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Merchant, Transaction
from datetime import datetime, timezone
from .schemas import TransactionCreate
from fastapi import HTTPException
from uuid import uuid4
from sqlalchemy.exc import SQLAlchemyError


# get_merchants
def get_merchants(db: Session):
    query = select(Merchant)
    result = db.execute(query)
    merchants = result.scalars().all()

    return merchants

# get_merchant
def get_merchant(db: Session, merchant_id: str):
    query = select(Merchant).where(Merchant.merchant_id == merchant_id)
    result = db.execute(query)
    merchant = result.scalar_one_or_none()

    return merchant


# Get transactions with optional filters
def get_transactions(
    db: Session,
    payment_status: str | None = None,
    merchant_id: str | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    # Assigning default for limit and offset
    limit: int = 100,
    offset: int = 0
):
    query = select(Transaction).limit(limit).offset(offset)

    if payment_status is not None:
        query = query.where(Transaction.payment_status == payment_status)

    if merchant_id is not None:
        query = query.where(Transaction.merchant_id == merchant_id)

    if start_datetime is not None:
        query = query.where(Transaction.transaction_date >= start_datetime)

    if end_datetime is not None:
        query = query.where(Transaction.transaction_date < end_datetime)

    result = db.execute(query)
    transactions = result.scalars().all()

    return transactions



def get_transaction(db: Session, transaction_id: str):
    query = select(Transaction).where(Transaction.transaction_id == transaction_id)
    result = db.execute(query)
    transaction = result.scalar_one_or_none()

    return transaction

def get_merchant_transactions(db: Session, merchant_id: str):
    query = select(Transaction).where(Transaction.merchant_id == merchant_id)
    result = db.execute(query)
    transactions = result.scalars().all()

    return transactions


# Create Transaction

def create_transaction(
    db: Session,
    transaction_data: TransactionCreate
):
    # 1. Check that the merchant exists
    merchant = get_merchant(db, transaction_data.merchant_id)

    if merchant is None:
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

    # 2. Create the transaction object
    new_transaction = Transaction(
        transaction_id=str(uuid4()),
        transaction_date=datetime.now(timezone.utc),
        merchant_id=transaction_data.merchant_id,
        card_type=transaction_data.card_type,
        transaction_amount=transaction_data.transaction_amount,
        payment_method=transaction_data.payment_method,
    )

    # 3. Save the transaction to PostgreSQL
    try:
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create transaction"
        )

    # 4. Return the created transaction
    return new_transaction