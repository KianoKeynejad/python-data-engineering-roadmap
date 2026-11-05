# Section 12 — Dependency Injection: Practice

# assumptions
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[str] = mapped_column(primary_key=True)
    merchant_name: Mapped[str]
    industry: Mapped[str | None]
    monthly_ttv: Mapped[float]
    is_active: Mapped[bool]



# 1. Write a simple Python function `get_database()` that returns `"Database connected"`.
# 2. Create a FastAPI route `/test` that uses `Depends(get_database)` to receive the result from `get_db()`.

from fastapi import FastAPI, Depends
from typing import Annotated
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

@app.get("/test")
def test(
    db: Annotated[Session, Depends(get_db)]
):
    return db


# 4. Create a dependency function**
# Create a dependency called `get_current_user()` that returns: {"user_id": 1, "name": "Kiano"}
# Use it in a `/profile` endpoint.

def get_current_user():
    return {
        "USER_id" : 1,
        "name" : "Kiano"
    }

@app.get("/profile")
def get_profile(user=Depends(get_current_user)):
    return user


# 5. Use `Annotated` with `Depends()`**
# Create a `/merchant` endpoint using:

# Annotated[..., Depends(...)]

# to inject a `get_merchant()` dependency.


def get_merchant():
    return {
        "id": 1,
        "name": "Kiano"
    }

@app.get("/merchant")
def get_merchant_details(
        merchant : Annotated[dict, Depends(get_merchant)]
):
    return merchant




"""
9. Create a GET /merchants endpoint that is ready to use a database session.

Build the endpoint so that:

SessionLocal creates database sessions
get_db() creates a session
get_db() uses yield
The session is closed after use
GET /merchants receives the session through Depends()
Use Annotated[Session, Depends(get_db)]
Do not query the database yet
Just return a simple message confirming the session was injected
"""


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/merchants")
def get_merchants(
    db: Annotated[Session, Depends(get_db)]
):
    print(db)
    return {"message": "Database session received"}

"""
10. Use the Injected Session

Using the db session received from Q9:

import select
query the Merchant model
use db.execute()
use .scalars().all()
return the merchants

"""
from sqlalchemy import select

@app.get("/merchants")
def get_merchants(
    db: Annotated[Session, Depends(get_db)]
):
    result = db.execute(
        select(Merchant)
    )

    merchants = result.scalars().all()

    return merchants

"""
12. Multiple dependencies - Create two dependencies:

get_db()
get_current_user()

Then create:

GET /merchants

and inject both into the same endpoint.
"""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user():
    return {
        "id": 1,
        "name": "Kiano"
    }

@app.get("/merchants")
def get_merchants(
        db : Annotated[Session, Depends(get_db)],
        user : Annotated[dict, Depends(get_current_user)]
):
    return db, user


"""
14. Complete Dependency Injection Flow

Build a small but complete Merchant API example containing:

create_engine()
SessionLocal
Session
get_db()
yield
try/finally
Depends()
Annotated
GET /merchants
injected database session
SQLAlchemy select()
db.execute()
scalars().all()
return the merchants
automatic session cleanup

"""
from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker


# Existing SQLAlchemy setup
DATABASE_URL = "postgresql://username:password@localhost:5432/payment_api"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


# Database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# FastAPI application
app = FastAPI()


# Merchant endpoint
@app.get("/merchants")
def get_merchants(
    db: Annotated[Session, Depends(get_db)]
):
    result = db.execute(
        select(Merchant)
    )

    merchants = result.scalars().all()

    return merchants

"""
SessionLocal
     ↓
get_db()
     ↓
Session created
     ↓
yield db
     ↓
Depends(get_db)
     ↓
db injected into endpoint
     ↓
db.execute(select(Merchant))
     ↓
merchants returned
     ↓
endpoint finishes
     ↓
finally
     ↓
db.close()
"""