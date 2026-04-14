from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class QuoteRead(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    text: str

    class Config:
        from_attributes = True


class QuoteCreate(BaseModel):
    text: str

    class Config:
        from_attributes = True


class QuoteUpdate(BaseModel):
    text: str | None = None

    class Config:
        from_attributes = True
