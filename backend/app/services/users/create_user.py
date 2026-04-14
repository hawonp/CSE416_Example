from uuid import UUID

from app.models.users import User
from app.schemas.users import UserCreate
from sqlalchemy.orm import Session


def create_new_user(db: Session, data: UserCreate) -> UUID:
    with db:
        user = User.create(data)
        db.add(user)
        db.commit()
        return user.id
