#  `models.py`   | Database layer            | **What the database table looks like**
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass

class Merchant(Base):
    __tablename__ = "merchants"
    merchant_id : Mapped[str] = mapped_column(primary_key=True)
    company_name : Mapped[str]
    mcc_code : Mapped[int]
    business_industry : Mapped[str]
    price_model : Mapped[str]
    msf_cc_percent: Mapped[float]
    msf_dc_dollar: Mapped[float]
    state: Mapped[str]
    postcode: Mapped[str]

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_date: Mapped[datetime] = mapped_column("Transaction Date")
    transaction_type: Mapped[str] = mapped_column("Transaction Type")
    card_type: Mapped[str] = mapped_column("Card Type")
    transaction_amount: Mapped[float] = mapped_column("Transaction Amount")
    purchase: Mapped[float] = mapped_column("Purchase")
    surcharge: Mapped[float] = mapped_column("Surcharge")
    payment_status: Mapped[str] = mapped_column("Payment Status")
    payment_method: Mapped[str] = mapped_column("Payment Method")
    merchant_id: Mapped[str] = mapped_column("Merchant ID")
    transaction_id: Mapped[str] = mapped_column("ID", primary_key=True)
    settlement_amount: Mapped[float] = mapped_column("Settlement Amount")


