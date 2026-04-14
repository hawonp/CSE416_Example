from collections.abc import Generator
from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import ReadOnlySession, ReadOnlySessionLocal, SessionLocal
from app.core.settings import SETTINGS
from app.models.users import User
from app.schemas.login import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{SETTINGS.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


def get_readonly_db() -> Generator[ReadOnlySession, None, None]:
    with ReadOnlySessionLocal() as session:
        session.execute(text("SET TRANSACTION READ ONLY"))
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
ReadOnlySessionDep = Annotated[ReadOnlySession, Depends(get_readonly_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


# def get_current_user(session: SessionDep, token: TokenDep) -> User:
#     try:
#         payload = jwt.decode(token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM])
#         token_data = TokenPayload(**payload)
#     except (InvalidTokenError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     user = session.get(User, token_data.sub)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return user


# CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_user_id(session: SessionDep, token: TokenDep) -> UUID:
    try:
        payload = jwt.decode(
            token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user.id


CurrentUserId = Annotated[UUID, Depends(get_current_user_id)]


def get_current_superuser_id(session: SessionDep, token: TokenDep) -> UUID:
    try:
        payload = jwt.decode(
            token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    if not user.is_superuser:
        raise HTTPException(
            status_code=403, detail="User does not have enough privileges"
        )
    return user.id
