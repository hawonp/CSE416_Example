from app.models.quotes import Quote
from app.schemas.quotes import QuoteUpdate
from faker import Faker

fake = Faker("ko_KR")


def test_update_quote():
    # arrange
    fake_quote = Quote(text=fake.text())
    fake_update_data = QuoteUpdate(
        text=fake.text(),
    )
    old_text = fake_quote.text

    # act
    fake_quote.update(fake_update_data)

    # assert
    assert fake_quote.text == fake_update_data.text
    assert fake_quote.text != old_text
