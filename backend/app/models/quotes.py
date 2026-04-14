from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.quotes import QuoteCreate, QuoteUpdate

from .base import Base

if TYPE_CHECKING:
    from .users import User


class Quote(Base):
    __tablename__ = "quote"

    text: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    #################
    # relationships #
    #################
    # see https://docs.sqlalchemy.org/en/21/orm/basic_relationships.html
    user: Mapped["User"] = relationship(
        "User",
        back_populates="quote",
        lazy="raise_on_sql",
        single_parent=True,
    )

    __table_args__ = (UniqueConstraint("user_id"),)

    ################
    # domain logic #
    ################
    @classmethod
    def create(
        cls,
        user_id: UUID,
        data: QuoteCreate,
    ) -> "Quote":
        return cls(
            id=uuid4(),
            text=data.text,
            user_id=user_id,
        )

    def update(
        self,
        data: QuoteUpdate,
    ) -> None:
        if data.text is not None:
            self.text = data.text

    def __str__(self) -> str:
        return f"Quote(id={self.id}, text={self.text}, user_id={self.user_id})"
