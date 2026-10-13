# | `services.py` | Business logic layer      | **What the application does with the data**           |

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Merchant, Transaction



def get_merchants(db: Session):
    query = select(Merchant)
    result = db.execute(query)
    merchants = result.scalars().all()

    return merchants

def get_merchant(db: Session, merchant_id: str):
    query = select(Merchant).where(Merchant.merchant_id == merchant_id)
    result = db.execute(query)
    merchant = result.scalar_one_or_none()

    return merchant

def get_transactions(db: Session):
    query = select(Transaction)
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