"""
Q1 — Raise a Basic HTTP Exception

Create a GET /merchant endpoint that always returns a 404 Not Found error with the message "Merchant not found".

"""

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/merchant")
def get_merchant():
    raise HTTPException(
        status_code=404,
        detail="Merchant not found"
    )

"""
Q2 — Return a 400 Bad Request

Create a GET /transactions endpoint that returns a 400 Bad Request with the message "Invalid transaction request".

"""

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/transactions")
def get_transactions():
    raise HTTPException(
        status_code=400,
        detail="Invalid transaction request"
    )

"""
Q3 — Use a Path Parameter with 404

Create:

GET /merchants/{merchant_id}

If the merchant_id is "M999", return a 404 error. Otherwise, return the merchant ID.

"""

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/merchants/{merchant_id}")
def get_merchant(merchant_id: str):

    if merchant_id == "M999":
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

    return {"merchant_id": merchant_id}

"""
Q4 — Check for a Missing Database Record

Assume db and the Merchant SQLAlchemy model already exist.

Create:

GET /merchants/{merchant_id}

Query PostgreSQL using SQLAlchemy. If the merchant doesn't exist, return 404.

"""

from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/merchants/{merchant_id}")
def get_merchant(
    merchant_id: str,
    db: Session
):
    merchant = db.execute(
        select(Merchant).where(Merchant.id == merchant_id)
    ).scalar_one_or_none()

    if merchant is None:
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

    return merchant

"""
Q5 — Validate a Transaction Amount

Create:

POST /transactions

If the transaction amount is less than or equal to 0, return 400 Bad Request.

"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Transaction(BaseModel):
    transaction_id: str
    merchant_id: str
    amount: float


@app.post("/transactions")
def create_transaction(transaction: Transaction):

    if transaction.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Transaction amount must be greater than 0"
        )

    return transaction

"""
Q6 — Merchant Not Found Before Creating Transaction

Create:

POST /merchants/{merchant_id}/transactions

Before creating the transaction, check whether the merchant exists. If not, return 404.

"""

from fastapi import FastAPI, HTTPException
from sqlalchemy import select

app = FastAPI()


@app.post("/merchants/{merchant_id}/transactions")
def create_transaction(
    merchant_id: str,
    transaction: Transaction,
    db: Session
):
    merchant = db.execute(
        select(Merchant).where(Merchant.id == merchant_id)
    ).scalar_one_or_none()

    if merchant is None:
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

    return transaction


"""
Q7 — Use try/except for a Database Error

Assume the database operation can raise an exception.

Catch the exception and return 500 Internal Server Error.

"""

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/merchants")
def get_merchants(db: Session):

    try:
        merchants = db.execute(
            select(Merchant)
        ).scalars().all()

        return merchants

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

"""
Q8 — Combine Query Parameters + 400

Create:

GET /transactions?limit=10

If limit is 0 or negative, return 400.

"""

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/transactions")
def get_transactions(limit: int | None = None):

    if limit is not None and limit <= 0:
        raise HTTPException(
            status_code=400,
            detail="Limit must be greater than 0"
        )

    return {"limit": limit}

"""
Q9 — Complete Merchant GET with 404

Create:

GET /merchants/{merchant_id}

Use:

get_db()
Depends()
SQLAlchemy
scalar_one_or_none()
HTTPException
404

Return the merchant if found.

"""

from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/merchants/{merchant_id}")
def get_merchant(
    merchant_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    merchant = db.execute(
        select(Merchant).where(Merchant.id == merchant_id)
    ).scalar_one_or_none()

    if merchant is None:
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

    return merchant

"""
Q10 — Complete Merchant List with Database Error Handling

Create:

GET /merchants

Use the database dependency and retrieve all merchants.

If a database error occurs, return 500.

"""

from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

app = FastAPI()


@app.get("/merchants")
def get_merchants(
    db: Annotated[Session, Depends(get_db)]
):
    try:
        result = db.execute(
            select(Merchant)
        )

        merchants = result.scalars().all()

        return merchants

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )

"""
Q11 — Understand the Error Flow

For:

if merchant is None:
    raise HTTPException(
        status_code=404,
        detail="Merchant not found"
    )

What happens after raise?

Answer:

The endpoint stops immediately.

The code below the raise is not executed.

FastAPI sends:

{
    "detail": "Merchant not found"
}

with:

HTTP 404 Not Found
"""



"""
Q12 — Final Merchant Endpoint

Create the complete:

GET /merchants/{merchant_id}

using:

Path parameter
Dependency Injection
SQLAlchemy
select()
scalar_one_or_none()
404 error
MerchantResponse

"""

from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

app = FastAPI()


class MerchantResponse(BaseModel):
    merchant_id: str
    merchant_name: str
    industry: str


@app.get(
    "/merchants/{merchant_id}",
    response_model=MerchantResponse
)
def get_merchant(
    merchant_id: str,
    db: Annotated[Session, Depends(get_db)]
):
    merchant = db.execute(
        select(Merchant).where(Merchant.id == merchant_id)
    ).scalar_one_or_none()

    if merchant is None:
        raise HTTPException(
            status_code=404,
            detail="Merchant not found"
        )

    return merchant