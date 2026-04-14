from uuid import uuid4

import pytest
from app.models.users import User
from app.schemas.users import UserUpdate
from faker import Faker

fake = Faker("ko_KR")


def test_update_user():
    # arrange
    fake_user = User(
        id=uuid4(),
        is_active=True,
        is_superuser=False,
    )

    fake_update_data = UserUpdate(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
    )

    # act
    fake_user.update(fake_update_data)

    # assert
    assert fake_user.firstname == fake_update_data.firstname
    assert fake_user.lastname == fake_update_data.lastname
    assert fake_user.email == fake_update_data.email
    assert fake_user.password != fake_update_data.password  # should be hashed
    assert fake_user.is_active is True
    assert fake_user.is_superuser is False


def test_update_user__short_password():
    # arrange
    fake_user = User(
        id=uuid4(),
        is_active=True,
        is_superuser=False,
    )

    fake_update_data = UserUpdate(
        password="short",
    )

    # act & assert
    with pytest.raises(ValueError):
        fake_user.update(fake_update_data)


def test_update_user__missing_digit():
    # arrange
    fake_user = User(
        id=uuid4(),
        is_active=True,
        is_superuser=False,
    )

    fake_update_data = UserUpdate(
        password="NoDigits!",
    )

    # act & assert
    with pytest.raises(ValueError):
        fake_user.update(fake_update_data)


def test_update_user__missing_uppercase():
    # arrange
    fake_user = User(
        id=uuid4(),
        is_active=True,
        is_superuser=False,
    )

    fake_update_data = UserUpdate(
        password="nouppercase1!",
    )

    # act & assert
    with pytest.raises(ValueError):
        fake_user.update(fake_update_data)


def test_update_user__missing_lowercase():
    # arrange
    fake_user = User(
        id=uuid4(),
        is_active=True,
        is_superuser=False,
    )

    fake_update_data = UserUpdate(
        password="NOLOWERCASE1!",
    )

    # act & assert
    with pytest.raises(ValueError):
        fake_user.update(fake_update_data)


def test_update_user__missing_special():
    # arrange
    fake_user = User(
        id=uuid4(),
        is_active=True,
        is_superuser=False,
    )

    fake_update_data = UserUpdate(
        password="NoSpecial1",
    )

    # act & assert
    with pytest.raises(ValueError):
        fake_user.update(fake_update_data)
