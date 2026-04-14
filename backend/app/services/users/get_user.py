from uuid import UUID

from sqlalchemy import Select, select, true
from sqlalchemy.orm import Session, selectinload

from app.models.users import User


def get_user_by_id(
    db: Session,
    user_id: UUID,
) -> User | None:
    with db:
        stmt: Select = (
            select(User)
            .options(
                selectinload(User.quote),
            )
            .where(
                User.id == user_id,
                User.is_active.is_(true()),
            )
        )

        user: User | None = db.execute(stmt).scalar_one_or_none()

        if user is None:
            raise ValueError(f"User with id {user_id} not found")

        return user


def get_all_users(db: Session) -> list[User]:
    with db:
        stmt: Select = (
            select(User)
            .options(
                selectinload(User.quote),
            )
            .where(
                User.is_active.is_(true()),
            )
            .order_by(User.id.asc(), User.created_at.asc())
        )

        users: list[User] = list(db.execute(stmt).scalars().all())

        return users
