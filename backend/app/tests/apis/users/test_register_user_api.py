from app.apis.v1.users import router
from app.core.settings import SETTINGS
from app.schemas.users import UserCreate
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient

faker = Faker("ko_KR")
API_V1_PREFIX = f"{SETTINGS.API_V1_STR}"


def test_register_user(
    test_client: TestClient,
    # login_token: dict,
):
    # arrange
    url = API_V1_PREFIX + router.url_path_for(
        "register_user",
    )
    create_data = UserCreate(
        firstname=faker.first_name(),
        lastname=faker.last_name(),
        email=faker.email(),
        password=faker.password(),
    )

    # act
    response = test_client.post(
        url,
        # headers=login_token,
        json=create_data.model_dump(exclude_unset=True),
    )

    # assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] is not None
    assert data["email"] == create_data.email
    assert data["firstname"] == create_data.firstname
    assert data["lastname"] == create_data.lastname
    assert data["quote"] is None
