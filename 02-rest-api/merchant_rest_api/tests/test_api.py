
import pytest
from fastapi.testclient import TestClient

from app.database import get_db
from app.main import app


# 1. Test the root endpoint
def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200


# 2. Test GET /merchants
def test_get_merchants(client):
    response = client.get("/merchants")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 3. Test GET /merchants/{merchant_id}
def test_get_merchant_by_id(client):
    merchants_response = client.get("/merchants")

    assert merchants_response.status_code == 200

    merchants = merchants_response.json()

    if not merchants:
        pytest.skip("No merchants available in the database")

    merchant_id = merchants[0]["merchant_id"]

    response = client.get(f"/merchants/{merchant_id}")

    assert response.status_code == 200
    assert response.json()["merchant_id"] == merchant_id


# 4. Test a merchant that does not exist
def test_get_missing_merchant(client):
    response = client.get(
        "/merchants/__missing_merchant_for_test__"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Merchant not found"


# 5. Test GET /transactions
def test_get_transactions(client):
    response = client.get("/transactions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 6. Test GET /transactions/{transaction_id}
def test_get_transaction_by_id(client):
    transactions_response = client.get("/transactions")

    assert transactions_response.status_code == 200

    transactions = transactions_response.json()

    if not transactions:
        pytest.skip("No transactions available in the database")

    transaction_id = transactions[0]["transaction_id"]

    response = client.get(
        f"/transactions/{transaction_id}"
    )

    assert response.status_code == 200
    assert response.json()["transaction_id"] == transaction_id


# 7. Test a transaction that does not exist
def test_get_missing_transaction(client):
    response = client.get(
        "/transactions/__missing_transaction_for_test__"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction not found"


# 8. Test GET /merchants/{merchant_id}/transactions
def test_get_merchant_transactions(client):
    merchants_response = client.get("/merchants")

    assert merchants_response.status_code == 200

    merchants = merchants_response.json()

    if not merchants:
        pytest.skip("No merchants available in the database")

    merchant_id = merchants[0]["merchant_id"]

    response = client.get(
        f"/merchants/{merchant_id}/transactions"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 9. Test transactions for a missing merchant
def test_get_transactions_for_missing_merchant(client):
    response = client.get(
        "/merchants/__missing_merchant_for_test__/transactions"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Merchant not found"


# 10. Test POST /transactions
def test_create_transaction(client):
    transaction_data = {
        "merchant_id": "SP7020000018176",
        "card_type": "DEBITCARD",
        "transaction_amount": 10.27,
        "payment_method": "Card",
    }

    response = client.post(
        "/transactions",
        json=transaction_data,
    )

    assert response.status_code == 201

    created_transaction = response.json()

    assert created_transaction["merchant_id"] == transaction_data["merchant_id"]
    assert created_transaction["transaction_amount"] == transaction_data["transaction_amount"]
    assert created_transaction["transaction_id"] is not None


# 11. Test request validation failure
def test_create_transaction_missing_required_fields(client):
    response = client.post(
        "/transactions",
        json={},
    )

    assert response.status_code == 422


# 12. Test invalid limit parameter
def test_transactions_invalid_limit(client):
    response = client.get("/transactions?limit=101")

    assert response.status_code == 422


# 13. Test invalid transaction ID
def test_transaction_id_too_long(client):
    long_transaction_id = "T" * 51

    response = client.get(
        f"/transactions/{long_transaction_id}"
    )

    assert response.status_code == 422


# 14. Test database dependency failure
def test_database_failure_returns_500(client):
    original_override = app.dependency_overrides.get(get_db)

    def broken_get_db():
        raise RuntimeError("Simulated database failure")
        yield

    app.dependency_overrides[get_db] = broken_get_db

    try:
        response = client.get("/merchants")

        assert response.status_code == 500

    finally:
        if original_override is None:
            app.dependency_overrides.pop(get_db, None)
        else:
            app.dependency_overrides[get_db] = original_override
