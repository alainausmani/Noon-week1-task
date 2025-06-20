import pytest
from sqlalchemy.orm import sessionmaker
from test.context import engine, Base
from test.auth.models.tables import User
from passlib.hash import bcrypt
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

@pytest.fixture(scope="function")
def db():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()  
@pytest.fixture
def create_test_user(db):
    user = User(
        email="forgot@example.com",
        password=bcrypt.hash("OriginalPass123"),
        first_name="Test",
        last_name="User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user