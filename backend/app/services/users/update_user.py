from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.users import UserUpdate


def update_existing_user(
    db: Session,
    user_id: UUID,
    data: UserUpdate,
) -> None:
    with db:
        stmt: Select = select(User).where(User.id == user_id)
        user: User | None = db.execute(stmt).scalar_one_or_none()

        if not user:
            raise ValueError(f"User with id {user_id} not found")

        user.update(data)
        db.add(user)
        db.commit()
