from uuid import UUID

from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.users import UserCreate


def create_new_user(db: Session, data: UserCreate) -> UUID:
    with db:
        user = User.create(data)
        db.add(user)
        db.commit()
        return user.id
