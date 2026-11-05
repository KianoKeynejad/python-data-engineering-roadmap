"""

| File / Folder | Purpose                    | Represents                                      |
|---------------|----------------------------|-------------------------------------------------|
| database.py   | Database connection layer  | How the application connects to PostgreSQL      |
|     ↓         |                            |                                                 |
| models.py     | Database model layer       | What the database tables look like              |
|     ↓         |                            | → What data do we have?                         |
|               |                            |                                                 |
| schemas.py    | API data validation layer  | What data the API accepts and returns           |
|               |                            | → What data do we expose?                       |
|     ↓         |                            | Schemas validate request structure and types,   |
|               |                            | and define the expected response structure.     |
|               |                            |                                                 |
| services.py   | Business / data access     | What the application does with the data         |
|               | logic layer                | → What do we do with the data?                  |
|               |                            | Contains database queries and business rules,   |
|     ↓         |                            | such as checking whether a merchant exists.     |
|               |                            |                                                 |
| routers/      | API endpoint layer         | How endpoints handle specific API requests      |
|               |                            | → Which endpoint handles the request?           |
|               |                            | merchants.py handles merchant-related endpoints |
|     ↓         |                            | transactions.py handles transaction endpoints.  |
|               |                            |                                                 |
| main.py       | Application entry point    | How the FastAPI application is created          |
|               |                            | and how routers are registered.                 |
|               |                            | → How are the API endpoints connected?          |

"""


#  http://127.0.0.1:8000/docs#/
import os
import logging
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from app.database import get_db
from app.routers import merchants, transactions
from fastapi.middleware.cors import CORSMiddleware

# LOGGING CONFIGURATION

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)


# FASTAPI APPLICATION INITIALISATION
app = FastAPI(
    title="Merchant REST API",
    version="1.0.0",
    debug=os.getenv("DEBUG", "false").lower() == "true",
    description=(
            "API for retrieving merchant information and managing "
            "payment transactions. Supports merchant lookups, "
            "transaction filtering, pagination and transaction creation."
        )
)

# CORS CONFIGURATION
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-API-Key"],
)


# ROUTER REGISTRATION
app.include_router(merchants.router)
app.include_router(transactions.router)


# TESTING THE APPLICATION
@app.get("/")
def root():
    return {"message": "Testing is done"}

from sqlalchemy import text


# Testing database connectivity
@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {"message": "Database connection successful"}

    except Exception:
        logger.exception("Database connection failed")

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )


