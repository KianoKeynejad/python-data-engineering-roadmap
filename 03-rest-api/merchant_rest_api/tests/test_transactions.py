from app.database import SessionLocal
from app.schemas import TransactionCreate
from app.services import create_transaction


def test_create_transaction():
    db = SessionLocal()

    try:
        transaction_data = TransactionCreate(
            merchant_id="SP7020000018176",
            card_type="DEBITCARD",
            transaction_amount=10.27,
            payment_method="Card",
        )

        transaction = create_transaction(db, transaction_data)

        assert transaction.merchant_id == "SP7020000018176"
        assert transaction.transaction_amount == 10.27
        assert transaction.transaction_id is not None

    finally:
        db.close()

