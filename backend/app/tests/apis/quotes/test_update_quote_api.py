from app.apis.v1.quotes import router
from app.core.settings import SETTINGS
from app.models.quotes import Quote
from app.models.users import User
from app.schemas.quotes import QuoteUpdate
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient

faker = Faker("ko_KR")
API_V1_PREFIX = f"{SETTINGS.API_V1_STR}"


def test_update_quote(
    test_client: TestClient,
    login_token: dict,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    user, quote = quote_dataset
    url = API_V1_PREFIX + router.url_path_for(
        "update_quote",
        quote_id=str(quote.id),
    )
    update_data = QuoteUpdate(
        text=faker.text(),
    )

    # act
    response = test_client.patch(
        url,
        headers=login_token,
        json=update_data.model_dump(exclude_unset=True),
    )

    # assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data is None
