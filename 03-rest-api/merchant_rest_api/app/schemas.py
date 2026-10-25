#  `schemas.py`  | API layer                 | **What data the API accepts/returns**                 |

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Annotated, Literal

# Define the structure and data types of a merchant API response
class MerchantResponse(BaseModel):
    merchant_id: str
    company_name: str
    mcc_code: int
    business_industry: str
    price_model: str
    msf_cc_percent: float
    msf_dc_dollar: float
    state: str
    postcode: str


# Test the MerchantResponse model
merchant = MerchantResponse(
    merchant_id="SP7020000018176",
    company_name="Example Business",
    mcc_code=5812,
    business_industry="Eating Places & Restaurants",
    price_model="SmartCharge",
    msf_cc_percent=0.70,
    msf_dc_dollar=0.20,
    state="NSW",
    postcode="2000"
)

print(merchant)

class TransactionResponse(BaseModel):
    transaction_date: datetime
    card_type: str
    transaction_amount: float
    payment_method: str
    merchant_id: str
    transaction_id: str


# Test the TransactionResponse model
transaction = TransactionResponse(
    transaction_date=datetime(2026, 5, 1, 10, 30, 0),
    card_type="Visa",
    transaction_amount=100.50,
    payment_method="Card",
    merchant_id="SP7020000018176",
    transaction_id="f80a8f42-a8f3-54c6-a6e5-c98732fb7a95",
)

print(transaction)

class TransactionCreate(BaseModel):
    merchant_id: str
    card_type: str
    transaction_amount: Annotated[float, Field(gt=0)]
    payment_method: Literal["Card"]

