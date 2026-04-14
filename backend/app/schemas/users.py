from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from .quotes import QuoteRead


class UserLogIn(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    firstname: str
    lastname: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserRead(UserLogIn):
    quote: QuoteRead | None = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    class Config:
        from_attributes = True
