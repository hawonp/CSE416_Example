from sqlalchemy import Select, select, true
from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.login import LoginPayload
from app.utils.security import verify_password


def authenticate_user(db: Session, data: LoginPayload) -> User | None:
    with db:
        # make statement
        stmt: Select = select(User).where(
            User.email == data.email,
            User.is_active.is_(true()),
        )

        # execute statement
        user: User | None = db.execute(stmt).scalar_one_or_none()

        # check if user exists
        if not user:
            raise ValueError(f"User with email {data.email} not found")

        # check if password is correct
        if not verify_password(data.password, user.password):
            raise ValueError("Incorrect Password")

        return user
