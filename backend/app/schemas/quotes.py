from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class QuoteRead(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    text: str

    model_config = ConfigDict(from_attributes=True)


class QuoteCreate(BaseModel):
    text: str

    model_config = ConfigDict(from_attributes=True)


class QuoteUpdate(BaseModel):
    text: str | None = None

    model_config = ConfigDict(from_attributes=True)
