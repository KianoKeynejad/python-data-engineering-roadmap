"""
Section 13 — FastAPI Fundamentals
Assumptions for all questions

We already have:

app = FastAPI()
Merchant Pydantic/SQLAlchemy models available when needed
Transaction models available when needed
get_db() dependency available when needed
Session and Depends() already understood


Q1 — Create a FastAPI Application

Create:

GET /

Return:

{"message": "Payment API"}
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Payment API"}


"""
Q2 — Create a Merchant Endpoint

Create:

GET /merchants

Return:

{"message": "List of merchants"}
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/merchants")
def get_merchants():
    return {"message": "List of merchants"}


"""
Q3 — Add a Path Parameter

Create:

GET /merchants/{merchant_id}

The endpoint should receive merchant_id and return it.

For:

GET /merchants/M001

return:

{"merchant_id": "M001"}
"""

@app.get("/merchant/{merchant_id}")
def get_merchant(
        merchant_id : str
):
    return {"merchant_id" : merchant_id}


"""
Q4 — Add a Second Path Parameter

Create:

GET /merchants/{merchant_id}/transactions/{transaction_id}

The endpoint should receive both IDs and return them.
"""
@app.get("/merchant/{merchant_id}/transactions/{transaction_id}")
def get_transaction(
        merchant_id : str,
        transaction_id : str
):
    return {
        "merchant_id" : merchant_id,
        "transaction_id" : transaction_id
    }


"""
🟡 Intermediate
Q5 — Add a Query Parameter

Create:

GET /transactions

with an optional:

?status=approved

Return the supplied status.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/transactions")
def get_transactions(status: str | None = None):
    return {"status": status}


"""
Q6 — Add Multiple Query Parameters

Create:

GET /transactions

with:

status
payment_method
limit

Example:

/transactions?status=approved&payment_method=card&limit=10

Return all three values.
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/transactions")
def get_transactions(
    status: str | None = None,
    payment_method: str | None = None,
    limit: int | None = None
):
    # "For this exercise, just show me what values FastAPI received."
    return {
        "status": status,
        "payment_method": payment_method,
        "limit": limit
    }

# Real project
#
# Later, the endpoint will look conceptually like:
#
# @app.get("/transactions")
# def get_transactions(
#     status: str | None = None,
#     payment_method: str | None = None,
#     limit: int | None = None,
#     db: Session = Depends(get_db)
# ):
#     # use status, payment_method and limit
#     # to query PostgreSQL
#
#     transactions = ...
#
#     return transactions
#
# And the client receives:
#
# [
#     {
#         "transaction_id": "T001",
#         "merchant_id": "M001",
#         "amount": 100.50
#     },
#     {
#         "transaction_id": "T002",
#         "merchant_id": "M002",
#         "amount": 250.00
#     }
# ]





"""
Q7 — Use a Path Parameter and a Query Parameter

Create:

GET /merchants/{merchant_id}/transactions

The endpoint should:

receive merchant_id as a path parameter
receive optional limit as a query parameter
return both values

For example:

GET /merchants/M001/transactions?limit=10

should return:

{
    "merchant_id": "M001",
    "limit": 10
}
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/merchants/{merchant_id}/transactions")
def get_transactions(
    merchant_id: str,
    limit: int | None = None
):
    return {
        "merchant_id": merchant_id,
        "limit": limit
    }


"""
Q8 — Create a Request Body

Create a Pydantic Transaction model containing:

transaction_id
merchant_id
amount
payment_method

Then create:

POST /transactions

Accept the transaction as the request body and return it.
"""
from pydantic import BaseModel

class Transaction(BaseModel):
    transaction_id: str
    merchant_id : str
    amount : float
    payment_method : str

@app.post("/transactions")
def create_transactions(transaction: Transaction):
    return transaction


"""
🔴 Difficult
Q9 — Create a Response Model

Create a Pydantic MerchantResponse model containing:

merchant_id
merchant_name
industry

Create:

GET /merchant

Use the Pydantic model as the response model and return one merchant.
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class MerchantResponse(BaseModel):
    merchant_id: str
    merchant_name: str
    industry: str

# response_model defines the structure of the data your API sends back to the client.

@app.get("/merchant", response_model=MerchantResponse)
def get_merchant():
    return {
        "merchant_id": "M001",
        "merchant_name": "ABC Cafe",
        "industry": "Restaurant"
    }

"""
|               | **Request Model**             | **Response Model**           |
| ------------- | ----------------------------- | ---------------------------- |
| Direction     | Client → API                  | API → Client                 |
| Purpose       | Defines what client **sends** | Defines what API **returns** |
| Example       | `Transaction`                 | `MerchantResponse`           |
| Main question | "What data do I accept?"      | "What data do I return?"     |
| FastAPI       | Function parameter            | `response_model=`            |

"""



"""
Q10 — Return Multiple Response Models

Create:

GET /merchants

Use a response model representing a list of merchants.

Return three merchants.
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class MerchantResponse(BaseModel):
    merchant_id: str
    merchant_name: str
    industry: str


@app.get("/merchants", response_model=list[MerchantResponse])
def get_merchants():
    return [
        {
            "merchant_id": "M001",
            "merchant_name": "ABC Cafe",
            "industry": "Restaurant"
        },
        {
            "merchant_id": "M002",
            "merchant_name": "XYZ Bakery",
            "industry": "Bakery"
        },
        {
            "merchant_id": "M003",
            "merchant_name": "Quick Eats",
            "industry": "Fast Food"
        }
    ]

"""
Q11 — Set an HTTP Status Code

Create:

POST /transactions

Use:

201 Created

when the transaction is successfully created.

Do not connect to the database.
"""

from fastapi import FastAPI, status

app = FastAPI()


@app.post("/transactions", status_code=status.HTTP_201_CREATED)
def create_transaction():
    return {"message": "Transaction created"}

"""
Q12 — Combine Path + Query + Request Body

Create:

POST /merchants/{merchant_id}/transactions

The endpoint should receive:

merchant_id → path parameter
source → query parameter
transaction → request body

Return all three.
"""
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Transaction(BaseModel):
    transaction_id: str
    amount: float
    payment_method: str


@app.post("/merchants/{merchant_id}/transactions")
def create_transaction(
    merchant_id: str,
    source: str | None = None,
    transaction: Transaction = None
):
    return {
        "merchant_id": merchant_id,
        "source": source,
        "transaction": transaction
    }

"""
Q13 — Merchant Transactions Endpoint

Create:

GET /merchants/{merchant_id}/transactions

The endpoint should:

receive merchant_id as a path parameter
receive optional limit as a query parameter
receive db through Depends(get_db)
do not query the database yet
simply return the received values
"""

from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://username:password@localhost:5432/payment_api"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/merchants/{merchant_id}/transactions")
def get_transactions(
    merchant_id: str,
    db: Annotated[Session, Depends(get_db)],
    limit: int | None = None
):
    return {
        "merchant_id": merchant_id,
        "limit": limit
    }

"""
Q14 — Complete FastAPI Flow

Build a small Merchant/Transaction API that demonstrates:

FastAPI()
GET
POST
path parameters
query parameters
request body
Pydantic model
response model
HTTP 201
Depends(get_db)
database session injection

"""
from typing import Annotated

from fastapi import FastAPI, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session


app = FastAPI()


# -------------------------
# Pydantic Models
# -------------------------

class MerchantResponse(BaseModel):
    merchant_id: str
    merchant_name: str
    industry: str


class Transaction(BaseModel):
    transaction_id: str
    amount: float
    payment_method: str


# -------------------------
# Database Dependency
# -------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# GET
# -------------------------

@app.get("/merchants", response_model=list[MerchantResponse])
def get_merchants(
    db: Annotated[Session, Depends(get_db)]
):
    return [
        {
            "merchant_id": "M001",
            "merchant_name": "ABC Cafe",
            "industry": "Restaurant"
        },
        {
            "merchant_id": "M002",
            "merchant_name": "XYZ Bakery",
            "industry": "Bakery"
        }
    ]


# -------------------------
# GET with Path + Query
# -------------------------

@app.get("/merchants/{merchant_id}/transactions")
def get_transactions(
    merchant_id: str,
    db: Annotated[Session, Depends(get_db)],
    limit: int | None = None
):
    return {
        "merchant_id": merchant_id,
        "limit": limit
    }


# -------------------------
# POST with Request Body
# -------------------------

@app.post(
    "/merchants/{merchant_id}/transactions",
    status_code=status.HTTP_201_CREATED
)
def create_transaction(
    merchant_id: str,
    transaction: Transaction,
    db: Annotated[Session, Depends(get_db)]
):
    return {
        "merchant_id": merchant_id,
        "transaction": transaction
    }