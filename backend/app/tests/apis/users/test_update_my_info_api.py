from app.apis.v1.users import router
from app.core.settings import SETTINGS
from app.models.users import User
from app.schemas.users import UserUpdate
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient

faker = Faker("ko_KR")
API_V1_PREFIX = f"{SETTINGS.API_V1_STR}"


def test_update_my_info(
    test_client: TestClient,
    login_token: dict,
    user_dataset: User,
):
    # arrange
    _ = user_dataset

    url = API_V1_PREFIX + router.url_path_for(
        "update_my_info",
    )

    # act
    response = test_client.patch(
        url,
        headers=login_token,
        json=UserUpdate(
            firstname=faker.first_name(),
            lastname=faker.last_name(),
            email=faker.email(),
            password=faker.password(),
        ).model_dump(exclude_unset=True),
    )

    # assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data is None
