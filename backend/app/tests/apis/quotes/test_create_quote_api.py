from app.apis.v1.quotes import router
from app.core.settings import SETTINGS
from app.models.users import User
from app.schemas.quotes import QuoteCreate
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient

faker = Faker("ko_KR")
API_V1_PREFIX = f"{SETTINGS.API_V1_STR}"


def test_create_quote(
    test_client: TestClient,
    login_token: dict,
    user_dataset: User,
):
    # arrange
    _ = user_dataset
    url = API_V1_PREFIX + router.url_path_for(
        "create_quote",
    )
    create_data = QuoteCreate(
        text=faker.text(),
    )

    # act
    response = test_client.post(
        url,
        headers=login_token,
        json=create_data.model_dump(exclude_unset=True),
    )

    # assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] is not None
