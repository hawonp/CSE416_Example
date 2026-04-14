from app.models.users import User
from app.schemas.users import UserCreate
from faker import Faker

fake = Faker("ko_KR")


def test_validate_password():
    # arrange
    fake_user_data = UserCreate(
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        email=fake.email(),
        password=fake.password(),
    )

    # act
    user = User.create(fake_user_data)

    # assert
    assert user.id is not None
    assert user.firstname == fake_user_data.firstname
    assert user.lastname == fake_user_data.lastname
    assert user.email == fake_user_data.email
    assert user.password != fake_user_data.password  # should be hashed
    assert user.is_active is True
    assert user.is_superuser is False
