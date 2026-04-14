from uuid import UUID

# from app.models.users import User
from app.models.quotes import Quote
from app.schemas.quotes import QuoteCreate
from sqlalchemy.orm import Session


def create_new_quote(
    db: Session,
    user_id: UUID,
    data: QuoteCreate,
) -> UUID:
    with db:
        quote = Quote.create(
            user_id=user_id,
            data=data,
        )
        db.add(quote)
        db.commit()
        return quote.id
