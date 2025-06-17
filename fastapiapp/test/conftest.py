import pytest
from sqlalchemy.orm import sessionmaker
from test.context import engine, Base
from test.auth.models.tables import User
from passlib.hash import bcrypt
# Create a session factory
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Create tables once before tests run
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    # ✅ Do NOT drop tables after
    yield

# ✅ Provide a database session for each test
@pytest.fixture(scope="function")
def db():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()  # only closes session, doesn't drop tables
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