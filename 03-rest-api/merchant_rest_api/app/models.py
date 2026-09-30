
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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

