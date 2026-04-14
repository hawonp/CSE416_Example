from app.apis.v1.quotes import router
from app.core.settings import SETTINGS
from app.models.quotes import Quote
from app.models.users import User
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient

faker = Faker("ko_KR")
API_V1_PREFIX = f"{SETTINGS.API_V1_STR}"


def test_delete_quote(
    test_client: TestClient,
    login_token: dict,
    quote_dataset: tuple[User, Quote],
):
    # arrange
    user, quote = quote_dataset
    url = API_V1_PREFIX + router.url_path_for(
        "delete_quote",
        quote_id=str(quote.id),
    )

    # act
    response = test_client.delete(
        url,
        headers=login_token,
    )

    # assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
