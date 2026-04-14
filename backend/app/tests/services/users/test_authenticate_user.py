import pytest
from app.models.users import User
from app.schemas.login import LoginPayload
from app.services.login.auth_user import authenticate_user
from app.utils.security import get_password_hash
from faker import Faker
from sqlalchemy.orm import Session

fake = Faker("ko_KR")


def test_authenticate_user(
    fake_db_session: Session,
    user_dataset: User,
):
    # arrange
    user = user_dataset
    user.password = get_password_hash("Password123!")  # set known password
    fake_db_session.commit()

    login_data = LoginPayload(
        email=user.email,
        password="Password123!",
    )

    # act
    result = authenticate_user(fake_db_session, login_data)

    # assert
    assert result is not None
    assert result.id == user.id
    assert result.email == user.email
    assert result.password == user.password


def test_authenticate_user__invalid_password(
    fake_db_session: Session,
    user_dataset: User,
):
    # arrange
    user = user_dataset
    login_data = LoginPayload(
        email=user.email,
        password="WrongPassword!",  # incorrect password
    )

    # act & assert
    with pytest.raises(ValueError):
        authenticate_user(fake_db_session, login_data)


def test_authenticate_user__inactive_user(
    fake_db_session: Session,
    user_dataset: User,
):
    # arrange
    user = user_dataset
    user.password = get_password_hash("Password123!")  # set known password
    user.is_active = False  # set user as inactive
    fake_db_session.commit()

    login_data = LoginPayload(
        email=user.email,
        password="Password123!",
    )

    # act & assert
    with pytest.raises(ValueError):
        authenticate_user(fake_db_session, login_data)


def test_authenticate_user__nonexistent_email(
    fake_db_session: Session,
):
    # arrange
    login_data = LoginPayload(
        email=fake.email(),  # email that doesn't exist in the database
        password="Password123!",
    )

    # act & assert
    with pytest.raises(ValueError):
        authenticate_user(fake_db_session, login_data)
