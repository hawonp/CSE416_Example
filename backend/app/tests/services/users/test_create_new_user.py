from uuid import UUID

import pytest
from app.models.users import User
from app.schemas.users import UserCreate
from app.services.users.create_user import create_new_user
from faker import Faker
from sqlalchemy import Select, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

fake = Faker("ko_KR")


def test_create_new_user(
    fake_db_session: Session,
):
    # arrange
    user_data = UserCreate(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
    )

    # act
    user_id: UUID = create_new_user(fake_db_session, user_data)

    # assert
    statement: Select = select(User).where(User.id == user_id)
    result: User = fake_db_session.execute(statement).scalar_one()

    assert result.id == user_id
    assert result.firstname == user_data.firstname
    assert result.lastname == user_data.lastname
    assert result.email == user_data.email
    assert result.password != user_data.password  # password should be hashed
    assert result.is_active is True
    assert result.is_superuser is False


def test_create_new_user__duplicate_email(
    fake_db_session: Session,
    user_dataset: User,
):
    # arrange
    user = user_dataset
    user_data = UserCreate(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        email=user.email,  # duplicate email
        password=fake.password(),
    )

    # act & assert
    with pytest.raises(IntegrityError):
        create_new_user(fake_db_session, user_data)
