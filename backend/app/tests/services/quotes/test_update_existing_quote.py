from uuid import uuid4

import pytest
from app.models.quotes import Quote
from app.models.users import User
from app.schemas.quotes import QuoteUpdate
from app.services.quotes.update_quote import update_existing_quote
from faker import Faker
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

fake = Faker("ko_KR")


def test_update_existing_quote(
    fake_db_session: Session,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    user, quote = quote_dataset
    update_data = QuoteUpdate(
        text=fake.text(),
    )

    # act
    update_existing_quote(
        fake_db_session,
        user.id,
        quote.id,
        update_data,
    )

    # assert
    statement: Select = select(Quote).where(Quote.id == quote.id)
    result: Quote = fake_db_session.execute(statement).scalar_one()

    assert result.id == quote.id
    assert result.text == update_data.text
    assert result.user_id == quote.user_id


def test_update_existing_quote__invalid_quote_id(
    fake_db_session: Session,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    user, _ = quote_dataset
    invalid_quote_id = uuid4()
    update_data = QuoteUpdate(
        text=fake.text(),
    )

    # act & assert
    with pytest.raises(ValueError):
        update_existing_quote(
            fake_db_session,
            user.id,
            invalid_quote_id,
            update_data,
        )


def test_update_existing_quote__invalid_user_id(
    fake_db_session: Session,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    _, quote = quote_dataset
    invalid_user_id = uuid4()
    update_data = QuoteUpdate(
        text=fake.text(),
    )

    # act & assert
    with pytest.raises(ValueError):
        update_existing_quote(
            fake_db_session,
            invalid_user_id,
            quote.id,
            update_data,
        )
