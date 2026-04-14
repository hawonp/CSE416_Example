from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from app.apis.dependencies import SessionDep
from app.core import security
from app.core.settings import SETTINGS
from app.schemas.login import LoginPayload, Token
from app.schemas.users import UserLogIn
from app.services.login.auth_user import authenticate_user

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/access-token")
def login_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        # authenticate user
        data = authenticate_user(
            session,
            LoginPayload(
                email=form_data.username,
                password=form_data.password,
            ),
        )

        # convert to dto
        dto = UserLogIn.model_validate(data)

        # create access token
        access_token_expires = timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(
            access_token=security.create_access_token(
                data={"sub": str(dto.id)},
                expires_delta=access_token_expires,
            )
        )

    except ValueError as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
