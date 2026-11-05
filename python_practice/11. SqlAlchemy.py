# SQLAlchemy Fundamentals — Practice Questions


# 1. Create a SQLAlchemy engine that connects to a PostgreSQL database called payment_api.
# Use a database URL in this format:
# postgresql://username:password@localhost:5432/payment_api

from sqlalchemy import create_engine

DATABASE_URL = "postgresql://username:password@localhost:5432/payment_api"
engine = create_engine(DATABASE_URL)
print(engine)

# Using SQLAlchemy, create a session factory that can be used to create database sessions.

from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
print(session)

# 3. Create a Merchant Database Model - Create a SQLAlchemy Merchant model representing this table:
# Use appropriate SQLAlchemy/Python types for each column.

# merchants
# ----------------
# id
# merchant_name
# industry
# monthly_ttv
# is_active

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

# 4. Add a Merchant Record - Using your Merchant SQLAlchemy model and a database session, create a new merchant:
# Add it to the session and commit the transaction.

# ID: M001
# Name: ABC Cafe
# Industry: Restaurant
# Monthly TTV: 125000.50
# Active: True

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


DATABASE_URL = "postgresql://username:password@localhost:5432/payment_api"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[str] = mapped_column(primary_key=True)
    merchant_name: Mapped[str]
    industry: Mapped[str | None]
    monthly_ttv: Mapped[float]
    is_active: Mapped[bool]


session = SessionLocal()

merchant = Merchant(
    id="M001",
    merchant_name="ABC Cafe",
    industry="Restaurant",
    monthly_ttv=125000.50,
    is_active=True
)

session.add(merchant)
session.commit()

print(merchant)




# 6. Retrieve Merchants for GET /merchants - Write a SQLAlchemy query that retrieves all merchants from the merchants table.
# The result should be suitable for the future:
# GET /merchants

from sqlalchemy import select

result = session.execute(
    select(Merchant)
)

merchants = result.scalars().all()
print(merchants)



# 7. Retrieve a Specific Merchant - Write a SQLAlchemy query to retrieve:
# merchant_id = "M001"
# This prepares you for:
# GET /merchants/{merchant_id}


result = session.execute(
    select(Merchant).where(Merchant.id == "M001")
)
merchant = result.scalar_one_or_none()

print(merchant)


# 8. Filter Merchants by Industry - Write a SQLAlchemy query that retrieves only:
# industry = "Restaurant"
#The filtering must happen in PostgreSQL through SQLAlchemy—not after retrieving everything into Python.

result = session.execute(
    select(Merchant).where(Merchant.industry == "Restaurant")
)
merchant = result.scalars().all()
print(merchant)




# 10. Retrieve a Merchant's Transactions - Create a SQLAlchemy Transaction model containing:

# transaction_id
# merchant_id
# amount
# payment_method
# status

# Then retrieve all transactions belonging to:
# merchant_id = "M001"

# This directly prepares you for: GET /merchants/{merchant_id}/transactions

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


DATABASE_URL = "postgresql://username:password@localhost:5432/payment_api"

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(bind=engine)


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id: Mapped[str] = mapped_column(primary_key=True)
    merchant_id: Mapped[str]
    amount: Mapped[float]
    payment_method: Mapped[str]
    status: Mapped[str]


session = LocalSession()

result = session.execute(
    select(Transaction).where(Transaction.merchant_id == "M001")
)

transactions = result.scalars().all()

print(transactions)


# 11. Retrieve High-Value Transactions - Retrieve transactions where: amount > 1000
# Then print:
# transaction_id
# amount
# This prepares you for the future transaction filtering in Phase 6 — Query Parameters.

from sqlalchemy import select

result = session.execute(
    select(Transaction).where(Transaction.amount > 1000)
)

transactions = result.scalars().all()

for transaction in transactions:
    print(transaction.transaction_id)
    print(transaction.amount)



# 12. Combine Merchant Filters - Retrieve merchants where:
# is_active = True
# monthly_ttv > 100000
# industry = "Restaurant"
# All conditions should be applied by the database query.
# This prepares you for combining multiple API filters later.

from sqlalchemy import select, and_

result = session.execute(
    select(Merchant).where(
        and_(
            Merchant.is_active == True,
            Merchant.monthly_ttv > 100000,
            Merchant.industry == "Restaurant"
        )
    )
)

merchants = result.scalars().all()

print(merchants)

# 13. Handle Merchant Not Found
# Query for:
# merchant_id = "M999"
# If no merchant is returned, print: Merchant not found
# This directly prepares you for the future:
# GET /merchants/{merchant_id}
#         ↓
# Merchant doesn't exist
#         ↓
# 404 Not Found
# We're only doing the database part now; FastAPI error handling comes later.

from sqlalchemy import select

result = session.execute(
    select(Merchant).where(Merchant.id == "M999")
)

merchant = result.scalar_one_or_none()

if merchant is None:
    print("Merchant not found")
else:
    print(merchant)



# 14. Complete Merchant Database Flow
#
# Build a small SQLAlchemy program that:
#
# 1. Connects to PostgreSQL
# 2. Creates a session
# 3. Creates a Merchant object
# 4. Adds it to the session
# 5. Commits it
# 6. Retrieves the merchant
# 7. Prints the merchant
#
# This brings together the core SQLAlchemy skills you'll actually need for Phase 3 — Merchant API.

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


# 1. Database connection
DATABASE_URL = "postgresql://username:password@localhost:5432/payment_api"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


# 2. Base class
class Base(DeclarativeBase):
    pass


# 3. Merchant model
class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[str] = mapped_column(primary_key=True)
    merchant_name: Mapped[str]
    industry: Mapped[str | None]
    monthly_ttv: Mapped[float]
    is_active: Mapped[bool]


# 4. Create database session
session = SessionLocal()


# 5. Create a merchant
merchant = Merchant(
    id="M001",
    merchant_name="ABC Cafe",
    industry="Restaurant",
    monthly_ttv=125000.50,
    is_active=True
)


# 6. Add merchant to session
session.add(merchant)


# 7. Save changes to database
session.commit()


# 8. Retrieve merchants
result = session.execute(
    select(Merchant)
)

merchants = result.scalars().all()


# 9. Print results
for merchant in merchants:
    print(
        merchant.id,
        merchant.merchant_name,
        merchant.industry,
        merchant.monthly_ttv,
        merchant.is_active
    )


# 10. Close session
session.close()