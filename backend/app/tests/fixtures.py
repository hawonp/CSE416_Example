from uuid import uuid4

import pytest
from faker import Faker
from sqlalchemy.orm import Session

from app.models.quotes import Quote
from app.models.users import User
from app.schemas.quotes import QuoteCreate
from app.schemas.users import UserCreate

fake = Faker("ko_KR")

FIXED_USER_ID = uuid4()


@pytest.fixture(scope="function")
def user_dataset(fake_db_session: Session) -> User:
    data = UserCreate(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
    )
    user = User.create(data)
    user.id = FIXED_USER_ID

    fake_db_session.add(user)
    fake_db_session.commit()

    return user


@pytest.fixture(scope="function")
def users_dataset(fake_db_session: Session) -> list[User]:
    users = []
    for _ in range(5):
        data = UserCreate(
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            email=fake.email(),
            password=fake.password(),
        )
        user = User.create(data)
        users.append(user)

    fake_db_session.add_all(users)
    fake_db_session.commit()

    return users


@pytest.fixture(scope="function")
def quote_dataset(
    fake_db_session: Session,
    user_dataset: User,
) -> tuple[User, Quote]:
    user = user_dataset
    data = QuoteCreate(
        text=fake.text(),
    )
    quote = Quote.create(
        user_id=user.id,
        data=data,
    )

    fake_db_session.add(quote)
    fake_db_session.commit()

    return user, quote
