from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, status
from loguru import logger

from app.apis.dependencies import (
    CurrentUserId,
    ReadOnlySessionDep,
    SessionDep,
    get_current_user_id,
)
from app.schemas.quotes import QuoteCreate, QuoteRead, QuoteUpdate
from app.services.quotes.create_quote import create_new_quote
from app.services.quotes.delete_quote import delete_existing_quote
from app.services.quotes.get_quote import get_quote_by_id
from app.services.quotes.update_quote import update_existing_quote

router = APIRouter(prefix="/quotes", tags=["quotes"])


@router.post(
    "/",
    dependencies=[Depends(get_current_user_id)],
    status_code=status.HTTP_201_CREATED,
    response_model=QuoteRead,
)
def create_quote(
    session: SessionDep,
    current_user_id: CurrentUserId,
    request_body: QuoteCreate = Body(...),
) -> QuoteRead:
    try:
        quote_id = create_new_quote(
            session,
            user_id=current_user_id,
            data=request_body,
        )
        quote = get_quote_by_id(
            db=session,
            quote_id=quote_id,
            user_id=current_user_id,
        )
        return QuoteRead.model_validate(quote)
    except ValueError as e:
        logger.error(f"Error creating quote: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch(
    "/{quote_id}",
    dependencies=[Depends(get_current_user_id)],
    status_code=status.HTTP_200_OK,
)
def update_quote(
    session: SessionDep,
    current_user_id: CurrentUserId,
    quote_id: UUID,
    request_body: QuoteUpdate = Body(...),
) -> None:
    try:
        update_existing_quote(
            db=session,
            user_id=current_user_id,
            quote_id=quote_id,
            data=request_body,
        )
    except ValueError as e:
        logger.error(f"Quote not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{quote_id}",
    dependencies=[Depends(get_current_user_id)],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_quote(
    session: SessionDep,
    current_user_id: CurrentUserId,
    quote_id: UUID,
) -> None:
    try:
        delete_existing_quote(
            db=session,
            user_id=current_user_id,
            quote_id=quote_id,
        )
    except ValueError as e:
        logger.error(f"Quote not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/{quote_id}",
    dependencies=[Depends(get_current_user_id)],
    status_code=status.HTTP_200_OK,
    response_model=QuoteRead,
)
def get_quote(
    session: ReadOnlySessionDep,
    current_user_id: CurrentUserId,
    quote_id: UUID,
) -> QuoteRead:
    try:
        quote = get_quote_by_id(
            db=session,
            quote_id=quote_id,
            user_id=current_user_id,
        )
        return QuoteRead.model_validate(quote)
    except ValueError as e:
        logger.error(f"Quote not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
