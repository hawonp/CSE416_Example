import http
from contextlib import asynccontextmanager

from app.apis.v1.login import router as login_router
from app.apis.v1.quotes import router as quotes_router
from app.apis.v1.users import router as users_router
from app.core.settings import SETTINGS
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from sqlalchemy.exc import DatabaseError
from starlette.requests import Request
from starlette.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    try:
        yield
    finally:
        try:
            logger.info("Shutting down...")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


# define the FastAPI app
app = FastAPI(
    title=SETTINGS.PROJECT_NAME,
    root_path=f"{SETTINGS.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)


# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=SETTINGS.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(
        f"Validation error at {request.method} {request.url.path}: {exc} | Query: {dict(request.query_params)}"
    )
    body = await request.body()
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "message": "Request validation failed",
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "body": body.decode() if body else None,
                "details": exc.errors(),
            }
        },
    )


@app.exception_handler(Exception)
async def api_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        f"Unhandled exception at {request.method} {request.url.path}: {exc} | Query: {dict(request.query_params)}"
    )

    body = None
    if request.method != "GET":
        body = await request.body()

    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": str(exc),
                "type": type(exc).__name__,
                "method": request.method,
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "body": body.decode() if body else None,
            }
        },
    )


@app.exception_handler(DatabaseError)
async def database_exception_handler(
    request: Request, exc: DatabaseError
) -> JSONResponse:
    # Extract SQLAlchemy details
    error_type = type(exc).__name__
    statement = getattr(exc, "statement", None)
    params = getattr(exc, "params", None)
    orig = getattr(
        exc, "orig", None
    )  # This is the original DB-API exception (e.g., from psycopg2)

    logger.error(f"SQLAlchemy DatabaseError: {error_type}")
    logger.error(f"Statement: {statement}")
    logger.error(f"Params: {params}")
    logger.error(f"Original error: {orig}")

    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "error_type": error_type,
            "statement": statement,
            "params": params,
            "orig": str(orig),
        },
    )


# heart beat endpoint
@app.get("/", status_code=status.HTTP_200_OK)
async def heartbeat() -> dict:
    return {"message": "Hello, World!"}


# import API routes
app.include_router(login_router, prefix=SETTINGS.API_V1_STR)
app.include_router(users_router, prefix=SETTINGS.API_V1_STR)
app.include_router(quotes_router, prefix=SETTINGS.API_V1_STR)
