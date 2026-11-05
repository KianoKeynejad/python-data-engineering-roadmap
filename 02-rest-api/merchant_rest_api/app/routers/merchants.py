
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import get_merchants, get_merchant, get_merchant_transactions
from app.schemas import MerchantResponse, TransactionResponse
from app.security import verify_api_key


router = APIRouter(
    dependencies=[Depends(verify_api_key)]
)

@router.get("/merchants", response_model=list[MerchantResponse])
def get_all_merchants(db: Session = Depends(get_db)):
    return get_merchants(db)


@router.get("/merchants/{merchant_id}", response_model=MerchantResponse)
def get_merchant_by_id(
    merchant_id: str = Path(min_length=1, max_length=50),
    db: Session = Depends(get_db)
):
    merchant = get_merchant(db, merchant_id)

    if merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")

    return merchant


@router.get(
    "/merchants/{merchant_id}/transactions",
    response_model=list[TransactionResponse],
)
def get_merchant_all_transactions(
    merchant_id: str = Path(min_length=1, max_length=50),
    db: Session = Depends(get_db),
):
    # check whether the merchant record exists
    merchant = get_merchant(db, merchant_id)

    if merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")

    return get_merchant_transactions(db, merchant_id)

