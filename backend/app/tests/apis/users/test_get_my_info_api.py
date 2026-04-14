from app.apis.v1.users import router
from app.core.settings import SETTINGS
from app.models.users import User
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient

faker = Faker("ko_KR")
API_V1_PREFIX = f"{SETTINGS.API_V1_STR}"


def test_get_my_info(
    test_client: TestClient,
    login_token: dict,
    user_dataset: User,
):
    # arrange
    user = user_dataset

    url = API_V1_PREFIX + router.url_path_for(
        "get_my_info",
    )

    # act
    response = test_client.get(
        url,
        headers=login_token,
    )

    # assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(user.id)
    assert data["email"] == user.email
    assert data["firstname"] == user.firstname
    assert data["lastname"] == user.lastname
    assert data["quote"] == user.quote
