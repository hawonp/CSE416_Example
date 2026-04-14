from contextlib import asynccontextmanager

from app.apis.v1.login import router as login_router
from app.apis.v1.quotes import router as quotes_router
from app.apis.v1.users import router as users_router
from app.core.settings import SETTINGS
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger


@asynccontextmanager
def lifespan(app: FastAPI):
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


# heart beat endpoint
@app.get("/", status_code=status.HTTP_200_OK)
def heartbeat() -> dict:
    return {"message": "Hello, World!"}


# import API routes
app.include_router(login_router, prefix=SETTINGS.API_V1_STR)
app.include_router(users_router, prefix=SETTINGS.API_V1_STR)
app.include_router(quotes_router, prefix=SETTINGS.API_V1_STR)
