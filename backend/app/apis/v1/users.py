from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from loguru import logger

from app.apis.dependencies import (
    CurrentUserId,
    ReadOnlySessionDep,
    SessionDep,
    get_current_superuser_id,
    get_current_user_id,
)
from app.schemas.users import UserCreate, UserRead, UserUpdate
from app.services.users.create_user import create_new_user
from app.services.users.get_user import get_all_users, get_user_by_id
from app.services.users.update_user import update_existing_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    dependencies=[Depends(get_current_superuser_id)],
    status_code=status.HTTP_200_OK,
    response_model=List[UserRead],
)
def get_users(
    session: ReadOnlySessionDep,
) -> List[UserRead]:
    data = get_all_users(session)
    return [UserRead.model_validate(user) for user in data]


@router.post(
    "/",
    dependencies=[Depends(get_current_superuser_id)],
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
)
def create_user(
    session: SessionDep,
    request_body: UserCreate = Body(...),
) -> UserRead:
    try:
        user_id = create_new_user(session, request_body)
        user = get_user_by_id(session, user_id)
        return UserRead.model_validate(user)
    except ValueError as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch(
    "/me",
    dependencies=[Depends(get_current_user_id)],
    status_code=status.HTTP_200_OK,
)
def update_my_info(
    session: SessionDep,
    current_user_id: CurrentUserId,
    request_body: UserUpdate = Body(...),
) -> None:
    try:
        user_id = current_user_id
        update_existing_user(session, user_id, request_body)
    except ValueError as e:
        logger.error(f"User not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/me",
    dependencies=[Depends(get_current_user_id)],
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
def get_my_info(
    session: ReadOnlySessionDep,
    current_user_id: CurrentUserId,
) -> UserRead:
    try:
        user_id = current_user_id
        user = get_user_by_id(session, user_id)
        return UserRead.model_validate(user)
    except ValueError as e:
        logger.error(f"User not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/signup",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    session: SessionDep,
    request_body: UserCreate = Body(...),
) -> UserRead:
    try:
        user_id = create_new_user(session, request_body)
        user = get_user_by_id(session, user_id)
        return UserRead.model_validate(user)
    except ValueError as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
