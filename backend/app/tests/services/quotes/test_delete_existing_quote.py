from uuid import uuid4

import pytest
from app.models.quotes import Quote
from app.models.users import User
from app.services.quotes.delete_quote import delete_existing_quote
from sqlalchemy import Select, select
from sqlalchemy.orm import Session


def test_delete_existing_quote(
    fake_db_session: Session,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    user, quote = quote_dataset

    # act
    delete_existing_quote(
        fake_db_session,
        user.id,
        quote.id,
    )

    # assert
    statement: Select = select(Quote).where(Quote.id == quote.id)
    result: Quote | None = fake_db_session.execute(statement).scalar_one_or_none()

    assert result is None


def test_delete_existing_quote__invalid_quote_id(
    fake_db_session: Session,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    user, _ = quote_dataset
    invalid_quote_id = uuid4()

    # act & assert
    with pytest.raises(ValueError):
        delete_existing_quote(
            fake_db_session,
            user.id,
            invalid_quote_id,
        )


def test_delete_existing_quote__invalid_user_id(
    fake_db_session: Session,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    _, quote = quote_dataset
    invalid_user_id = uuid4()

    # act & assert
    with pytest.raises(ValueError):
        delete_existing_quote(
            fake_db_session,
            invalid_user_id,
            quote.id,
        )
