from uuid import uuid4

import pytest
from app.models.users import User
from app.schemas.users import UserUpdate
from app.services.users.update_user import update_existing_user
from faker import Faker
from sqlalchemy import Select, select
from sqlalchemy.orm import Session

fake = Faker("ko_KR")


def test_update_existing_user(
    fake_db_session: Session,
    user_dataset: User,
):
    # arrange
    user = user_dataset
    update_data = UserUpdate(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
    )

    # act
    update_existing_user(fake_db_session, user.id, update_data)

    # assert
    statement: Select = select(User).where(User.id == user.id)
    result: User = fake_db_session.execute(statement).scalar_one()
    assert result.id == user.id
    assert result.firstname == update_data.firstname
    assert result.lastname == update_data.lastname
    assert result.email == update_data.email
    assert result.password != update_data.password  # password should be hashed
    assert result.is_active is True
    assert result.is_superuser is False


def test_update_existing_user__nonexistent_user(
    fake_db_session: Session,
):
    # arrange
    non_existent_user_id = uuid4()
    update_data = UserUpdate(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
    )

    # act & assert
    with pytest.raises(ValueError):
        update_existing_user(fake_db_session, non_existent_user_id, update_data)
