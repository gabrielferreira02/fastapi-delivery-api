import pytest
from app.models.user import User
from app.models.base import Base
from tests.test_database import engine, TestingSessionLocal
from uuid import uuid4

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def create_user():
    def _create_user(session):
        user = User(
            f"first_name_{uuid4()}",
            f"first_name_{uuid4()}",
            f"{uuid4()}@email.com",
            "12345678",
            False
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    return _create_user