
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.main import app


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    db = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app, raise_server_exceptions=False) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
