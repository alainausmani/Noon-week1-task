import pytest
from src.libauth.Loginuser.domain.user import login_user
from src.libauth.RegisterUser.domain.user import create_user
from test.auth.models.tables import User
from src.libauth.messages import UserRegistrationRequest, UserLoginRequest
from src.libauth.messages import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ResetTokenResponse,
    UserRegistrationRequest,
    UserLoginRequest
)
from src.libauth.ForgotPassword.domain.user import (
    forgot_password,
    reset_password,
    generate_reset_token
)

def test_user_registration_success(db):
    request = UserRegistrationRequest(
        email="test1@example.com",
        password="StrongPass123",
        first_name="Test",
        last_name="User"
    )
    response = create_user(db, request)
    assert response.email == "test1@example.com"
    assert response.first_name == "Test"
    assert response.last_name == "User"
    assert hasattr(response, "id")

def test_user_registration_duplicate_email(db):
    db.query(User).filter(User.email == "test1@example.com").delete()
    db.commit()

    request = UserRegistrationRequest(
        email="test1@example.com",
        password="StrongPass123",
        first_name="Test",
        last_name="User"
    )
    create_user(db, request)  # First registration

    with pytest.raises(ValueError) as exc_info:
        create_user(db, request)  # Second registration should fail
    assert "Email is already registered" in str(exc_info.value)


# ✅ Test successful login
def test_user_login_success(db):
    reg = UserRegistrationRequest(
        email="loginuser@example.com",
        password="MySecurePass!",
        first_name="Log",
        last_name="In"
    )
    create_user(db, reg)

    login = UserLoginRequest(
        email="loginuser@example.com",
        password="MySecurePass!"
    )

    response = login_user(db, login)
    assert response.token_type == "bearer"
    assert response.access_token is not None
    assert response.expires_in == 60

# ❌ Test login with invalid password
def test_user_login_invalid_password(db):
    reg = UserRegistrationRequest(
        email="failuser@example.com",
        password="CorrectPass123",
        first_name="Wrong",
        last_name="Pass"
    )
    create_user(db, reg)

    login = UserLoginRequest(
        email="failuser@example.com",
        password="WrongPass"  # incorrect password
    )

    with pytest.raises(Exception) as exc_info:
        login_user(db, login)
    assert "Invalid email or password" in str(exc_info.value)

def test_reset_password_success(db):
    # Clean up user if already exists
    db.query(User).filter(User.email == "reset1@example.com").delete()
    db.commit()

    # Create user
    user = User(
        email="reset1@example.com",
        password=bcrypt.hash("OldPassword123"),
        first_name="Reset",
        last_name="User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = generate_reset_token("reset1@example.com")
    request = ResetPasswordRequest(token=token, new_password="NewSecurePass123")
    response = reset_password(db, request)
    assert response["message"] == "Password reset successful"

def test_forgot_password_user_not_found(db):
    request = ForgotPasswordRequest(email="nonexistent@example.com")
    with pytest.raises(Exception) as exc_info:
        forgot_password(db, request)
    assert "User not found" in str(exc_info.value)

def test_reset_password_success(db, create_test_user):
    token = generate_reset_token("forgot@example.com")
    request = ResetPasswordRequest(token=token, new_password="NewSecurePass123")
    response = reset_password(db, request)
    assert response["message"] == "Password reset successful"

def test_reset_password_invalid_token(db):
    request = ResetPasswordRequest(token="invalid.token.here", new_password="StrongPass123")
    with pytest.raises(Exception) as exc_info:
        reset_password(db, request)
    assert "Invalid or expired token" in str(exc_info.value)