
from datetime import datetime

from fastapi import APIRouter, Depends, Path, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import (
    get_transactions,
    get_transaction,
    create_transaction,
)
from app.schemas import TransactionResponse, TransactionCreate

router = APIRouter()


@router.get("/transactions", response_model=list[TransactionResponse])
def get_all_transactions(
    db: Session = Depends(get_db),
    payment_status: str | None = None,
    merchant_id: str | None = None,
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    limit: int = Query(default=100, ge=0, le=100),
    offset: int = Query(default=0, ge=0),
):
    return get_transactions(
        db,
        payment_status,
        merchant_id,
        start_datetime,
        end_datetime,
        limit,
        offset,
    )


@router.get(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction_by_id(
    transaction_id: str = Path(min_length=1, max_length=50),
    db: Session = Depends(get_db),
):
    transaction = get_transaction(db, transaction_id)

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction


@router.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=201,
)
def create_transaction_endpoint(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
):
    return create_transaction(db, transaction_data)
