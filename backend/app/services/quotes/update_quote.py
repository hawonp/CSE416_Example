from uuid import UUID

from app.models.quotes import Quote
from app.schemas.quotes import QuoteUpdate
from sqlalchemy import Select, select
from sqlalchemy.orm import Session


def update_existing_quote(
    db: Session,
    user_id: UUID,
    quote_id: UUID,
    data: QuoteUpdate,
) -> None:
    with db:
        stmt: Select = select(Quote).where(
            Quote.id == quote_id,
            Quote.user_id == user_id,
        )
        quote: Quote | None = db.execute(stmt).scalar_one_or_none()

        if not quote:
            raise ValueError(f"Quote with id {quote_id} not found")

        quote.update(data)
        db.add(quote)
        db.commit()
