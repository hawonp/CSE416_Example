from uuid import uuid4

import pytest
from app.models.quotes import Quote
from app.models.users import User
from app.services.quotes.get_quote import get_quote_by_id
from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import DetachedInstanceError

fake = Faker("ko_KR")


def test_get_quote_by_id(
    fake_db_session: Session,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    user, quote = quote_dataset

    # act
    result = get_quote_by_id(
        fake_db_session,
        user.id,
        quote.id,
    )

    # assert
    assert result is not None
    assert result.id == quote.id
    assert result.text == quote.text
    assert result.user_id == user.id

    with pytest.raises(DetachedInstanceError):
        result.user  # should be detached from session, so accessing user should raise error


def test_get_quote_by_id__invalid_user_id(
    fake_db_session: Session,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    _, quote = quote_dataset
    invalid_user_id = uuid4()

    # act & assert
    with pytest.raises(ValueError):
        get_quote_by_id(
            fake_db_session,
            invalid_user_id,
            quote.id,
        )


def test_get_quote_by_id__invalid_quote_id(
    fake_db_session: Session,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    user, _ = quote_dataset
    invalid_quote_id = uuid4()

    # act & assert
    with pytest.raises(ValueError):
        get_quote_by_id(
            fake_db_session,
            user.id,
            invalid_quote_id,
        )
