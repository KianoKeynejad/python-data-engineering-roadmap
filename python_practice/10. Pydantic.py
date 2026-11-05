# Pydantic practice Qs ( pydantic is python class with validation data )

# 🟢 Easy
# 1. Create a Pydantic Merchant model with name, industry, and is_active fields using appropriate types.
from pydantic import BaseModel

class MerchantResponse(BaseModel):
    name: str
    industry: str
    is_active: bool

# 4. Create a Pydantic PaymentMethod model containing name and fee_rate. Create an object representing a credit-card payment method.

class PaymentMethod(BaseModel):
    name: str
    fee_rete: float

credit_card = PaymentMethod(
    name="credit Card",
    fee_rete=0.02
)

# 🟡 Intermediate
# 5. Create a Merchant model where industry is optional. Create one merchant with an industry and another merchant without one.

class MerchantResponse(BaseModel):
    name: str
    merchant_id: str
    industry: str | None = None

merchant1 = MerchantResponse(
    name=" ali",
    merchant_id="123456",
    industry="Bakery"
)
merchant2 = MerchantResponse(
    name=" ali",
    merchant_id="123456"
)


# 7. Create a Merchant model containing name, monthly_ttv, and is_active. Add basic validation so that monthly_ttv cannot be negative.

from pydantic import BaseModel, Field

class Merchant(BaseModel):
    name: str
    monthly_TTV: float = Field(gt=0)
    is_active: bool


# 8. Create a PricingDeal Pydantic model containing merchant_id, fee_percentage, and fixed_fee. Add validation so that both fees cannot be negative.

from typing import Annotated
from pydantic import BaseModel, Field

class PricingDeal(BaseModel):
    merchant_id: str
    fee_percentage: Annotated[float, Field(gt=0)]
    fixed_rate: Annotated[float, Field(gt=0)]

# 🔴 Difficult
# 9. Create a Pydantic model representing a POST /transactions request for your payment API. Include the important transaction fields and appropriate required/optional fields.

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated

class Transaction(BaseModel):
    transaction_id: str
    transaction_type: str | None = None
    amount: Annotated[float, Field(gt=0)]

app = FastAPI()
@app.post("/transactions/")
def post_transaction( transaction: Transaction ):
    return transaction



# 10. Create a Pydantic Merchant model and convert a valid merchant object into a Python dictionary using Pydantic's model conversion functionality.

from pydantic import BaseModel, Field

class MerchantResponse(BaseModel):
    name: str
    merchant_id: str
    industry: str | None = None
    monthly_TTV: float = Field(gt=0)

merchant = MerchantResponse(
    name=" ali",
    merchant_id="123456",
    industry="Bakery",
    monthly_TTV=0.02
)

merchant_dict = merchant.model_dump()
print(merchant_dict)

# 11. Create a Pydantic Transaction model with validation requiring:
# amount greater than 0
# payment method to be provided
# transaction ID to be provided

# Test the model with both valid and invalid data.

from pydantic import BaseModel, Field
from typing import Annotated

PaymentMethod = ["credit card", "Debit Card"]


class Transaction(BaseModel):
    transaction_id: str
    amount: Annotated[float, Field(gt=0)]
    payment_method: str = PaymentMethod

transaction = Transaction(
    transaction_id="TXN001",
    amount=250.50,
    payment_method="Credit Card"
)

print(transaction)

# Invalid transaction
invalid_transaction = Transaction(
    transaction_id="TXN002",
    amount=-50,
    payment_method="Credit Card"
)

print(invalid_transaction)




# 14.Build a small Pydantic-based payment request validation example.
# Accept merchant information and transaction information, validate the incoming data, and convert the validated Pydantic model into dictionary data ready to be used by your service/database layer.layer

from pydantic import BaseModel,Field
from typing import Annotated

class MerchantResponse(BaseModel):
    name: str
    merchant_id: str
    industry: str | None = None
    monthly_TTV: Annotated[float, Field(gt=0)]

class Transaction(BaseModel):
    transaction_id: str
    amount: Annotated[float, Field(gt=0)]
    payment_method: str


class PaymentRequest(BaseModel):
    merchant: Merchant
    transaction: Transaction

"""
PaymentRequest is the model definition, not the object and PaymentRequest is the class.

You need to first create an actual PaymentRequest object:

payment_request = PaymentRequest(
    merchant=...,
    transaction=...
)

Then you can do:

payment_data = payment_request.model_dump()
"""

payment_request = PaymentRequest(
    merchant=MerchantResponse(
        name=" ali",
        merchant_id="123456",
        industry="Bakery",
        monthly_TTV=400000
    ),
    transaction=Transaction(
        transaction_id="TXN001",
        amount=250.50,
        payment_method="Credit Card"
    )
)
payment_data = payment_request.model_dump()
print(payment_request)

