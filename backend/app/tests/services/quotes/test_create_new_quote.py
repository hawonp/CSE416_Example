from uuid import UUID, uuid4

import pytest
from app.models.quotes import Quote
from app.models.users import User
from app.schemas.quotes import QuoteCreate
from app.services.quotes.create_quote import create_new_quote
from faker import Faker
from sqlalchemy import Select, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

fake = Faker("ko_KR")


def test_create_new_quote(
    fake_db_session: Session,
    user_dataset: User,
):
    # arrange
    user = user_dataset
    quote_data = QuoteCreate(
        text=fake.text(),
    )

    # act
    quote_id: UUID = create_new_quote(fake_db_session, user.id, quote_data)

    # assert
    statement: Select = select(Quote).where(Quote.id == quote_id)
    result: Quote = fake_db_session.execute(statement).scalar_one()

    assert result.id == quote_id
    assert result.text == quote_data.text
    assert result.user_id == user.id


def test_create_new_quote__invalid_user_id(
    fake_db_session: Session,
):
    # arrange
    invalid_user_id = uuid4()
    quote_data = QuoteCreate(
        text=fake.text(),
    )

    # act & assert
    with pytest.raises(IntegrityError):
        create_new_quote(
            fake_db_session,
            invalid_user_id,
            quote_data,
        )
