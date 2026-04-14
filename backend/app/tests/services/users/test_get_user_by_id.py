from uuid import uuid4

import pytest
from app.models.quotes import Quote
from app.models.users import User
from app.services.users.get_user import get_user_by_id
from faker import Faker
from sqlalchemy.orm import Session

fake = Faker("ko_KR")


def test_get_user_by_id(
    fake_db_session: Session,
    user_dataset: User,
):
    # arrange
    user = user_dataset

    # act
    result = get_user_by_id(fake_db_session, user.id)

    # assert
    assert result is not None
    assert result.id == user.id
    assert result.firstname == user.firstname
    assert result.lastname == user.lastname
    assert result.email == user.email
    assert result.password == user.password  # password should be hashed
    assert result.is_active is True
    assert result.is_superuser is False
    assert result.quote is None


def test_get_user_by_id__with_quote(
    fake_db_session: Session,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    user, quote = quote_dataset

    # act
    result = get_user_by_id(fake_db_session, user.id)

    # assert
    assert result is not None
    assert result.id == user.id
    assert result.firstname == user.firstname
    assert result.lastname == user.lastname
    assert result.email == user.email
    assert result.password == user.password  # password should be hashed
    assert result.is_active is True
    assert result.is_superuser is False
    assert result.quote.id == quote.id
    assert result.quote.text == quote.text


def test_get_user_by_id__invalid_id(
    fake_db_session: Session,
):
    # arrange
    invalid_user_id = uuid4()

    # act & assert
    with pytest.raises(ValueError):
        get_user_by_id(fake_db_session, invalid_user_id)


def test_get_user_by_id__inactive_user(
    fake_db_session: Session,
    user_dataset: User,
):
    # arrange
    user = user_dataset

    # statement: Update = update(User).where(User.id == user.id).values(is_active=False)
    # fake_db_session.execute(statement)

    user.is_active = False
    fake_db_session.commit()

    # act & assert
    with pytest.raises(ValueError):
        get_user_by_id(fake_db_session, user.id)
