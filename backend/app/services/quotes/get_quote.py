from uuid import UUID

from app.models.quotes import Quote
from sqlalchemy import Select, select
from sqlalchemy.orm import Session


def get_quote_by_id(
    db: Session,
    user_id: UUID,
    quote_id: UUID,
) -> Quote | None:
    with db:
        stmt: Select = select(Quote).where(
            Quote.id == quote_id,
            Quote.user_id == user_id,
        )

        quote: Quote | None = db.execute(stmt).scalar_one_or_none()

        if quote is None:
            raise ValueError(f"Quote with id {quote_id} not found")

        return quote
