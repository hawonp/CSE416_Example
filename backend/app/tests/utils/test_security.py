from datetime import timedelta

from app.utils.security import create_access_token, verify_password
from faker import Faker
from pwdlib import PasswordHash

fake = Faker("ko_KR")
password_hash = PasswordHash.recommended()


def test_verify_password():
    fake_password = fake.password()
    hashed_password = password_hash.hash(fake_password)

    assert verify_password(fake_password, hashed_password)


def test_create_access_token():
    data = {"sub": "test_user_id"}
    expires_delta = timedelta(minutes=15)

    token = create_access_token(data=data, expires_delta=expires_delta)

    assert token is not None
