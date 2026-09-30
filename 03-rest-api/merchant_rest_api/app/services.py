from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Merchant

def get_merchants(db :Session):
    query = select(Merchant)
    result = db.execute(query)
    merchants = result.scalars().all()

    return merchants

def get_merchant(db: Session, merchant_id: str):
    query = select(Merchant).where(Merchant.merchant_id == merchant_id)
    result = db.execute(query)
    merchant = result.scalar_one_or_none()

    return merchant