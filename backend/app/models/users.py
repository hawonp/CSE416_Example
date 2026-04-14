from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.users import UserCreate, UserUpdate
from app.utils.security import get_password_hash

from .base import Base

if TYPE_CHECKING:
    from .quotes import Quote


class User(Base):
    __tablename__ = "user"

    firstname: Mapped[str]
    lastname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    #################
    # relationships #
    #################
    quote: Mapped["Quote"] = relationship(
        "Quote",
        back_populates="user",
        lazy="raise_on_sql",
        cascade="all, delete",
        passive_deletes=True,
    )

    ################
    # domain logic #
    ################

    @classmethod
    def create(cls, data: UserCreate) -> "User":
        User().validate_password(data.password)
        return cls(
            id=uuid4(),
            firstname=data.firstname,
            lastname=data.lastname,
            email=data.email,
            password=get_password_hash(data.password),
            is_active=True,
            is_superuser=False,
        )

    def update(self, data: UserUpdate) -> None:
        if data.firstname is not None:
            self.firstname = data.firstname
        if data.lastname is not None:
            self.lastname = data.lastname
        if data.email is not None:
            self.email = data.email
        if data.password is not None:
            self.validate_password(data.password)
            self.password = get_password_hash(data.password)

    def validate_password(self, password: str) -> None:
        is_valid_length = len(password) >= 8
        has_digits = any(char.isdigit() for char in password)
        has_uppercase = any(char.isupper() for char in password)
        has_lowercase = any(char.islower() for char in password)
        has_special = any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in password)

        if not (
            is_valid_length
            and has_digits
            and has_uppercase
            and has_lowercase
            and has_special
        ):
            raise ValueError(
                "Password must be at least 8 characters long and contain at least one digit, one uppercase letter, one lowercase letter, and one special character."
            )

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, firstname={self.firstname}, lastname={self.lastname})"
