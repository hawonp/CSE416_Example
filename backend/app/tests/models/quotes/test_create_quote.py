from uuid import uuid4

from app.models.quotes import Quote
from app.schemas.quotes import QuoteCreate
from faker import Faker

fake = Faker("ko_KR")


def test_create_quote():
    # arrange
    fake_user_id = uuid4()
    fake_quote_data = QuoteCreate(
        text=fake.text(),
    )

    # act
    quote = Quote.create(
        user_id=fake_user_id,
        data=fake_quote_data,
    )

    # assert
    assert quote.id is not None
    assert quote.text == fake_quote_data.text
    assert quote.user_id == fake_user_id
