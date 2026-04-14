from app.models.users import User
from app.services.users.get_user import get_all_users
from faker import Faker
from sqlalchemy.orm import Session

fake = Faker("ko_KR")


def test_get_all_users(
    fake_db_session: Session,
    users_dataset: list[User],
):
    # arrange
    users = users_dataset

    # act
    result = get_all_users(fake_db_session)

    # assert
    sorted_users = sorted(users, key=lambda u: u.id)
    sorted_result = sorted(result, key=lambda u: u.id)

    assert len(result) == len(users)
    for res_user, user in zip(sorted_result, sorted_users):
        assert res_user.id == user.id
        assert res_user.firstname == user.firstname
        assert res_user.lastname == user.lastname
        assert res_user.email == user.email
        assert res_user.password == user.password  # password should be hashed
        assert res_user.is_active is True
        assert res_user.is_superuser is False


def test_get_all_users__no_users(
    fake_db_session: Session,
):
    # arrange
    # no users in the database

    # act
    result = get_all_users(fake_db_session)

    # assert
    assert isinstance(result, list)
    assert len(result) == 0


def test_get_all_users__inactive_users(
    fake_db_session: Session,
    users_dataset: list[User],
):
    # arrange
    users = users_dataset
    for user in users:
        user.is_active = False
        fake_db_session.add(user)
    fake_db_session.commit()

    # act
    result = get_all_users(fake_db_session)

    # assert
    assert isinstance(result, list)
    assert len(result) == 0
