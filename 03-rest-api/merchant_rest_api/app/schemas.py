#  `schemas.py`  | API layer                 | **What data the API accepts/returns**                 |

from pydantic import BaseModel
from datetime import datetime


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
    transaction_type: str
    card_type: str
    transaction_amount: float
    purchase: float
    surcharge: float
    payment_status: str
    payment_method: str
    merchant_id: str
    transaction_id: str
    settlement_amount: float

# Test the TransactionResponse model
transaction = TransactionResponse(
    transaction_date=datetime(2026, 5, 1, 10, 30, 0),
    transaction_type="Purchase",
    card_type="Visa",
    transaction_amount=100.50,
    purchase=100.00,
    surcharge=0.50,
    payment_status="Approved",
    payment_method="Card",
    merchant_id="SP7020000018176",
    transaction_id="f80a8f42-a8f3-54c6-a6e5-c98732fb7a95",
    settlement_amount=100.50
)

print(transaction)

