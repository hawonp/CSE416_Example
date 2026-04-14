import secrets

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    # base settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "CSE416 Example"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # database settings
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # return str(
        #     MultiHostUrl.build(
        #         scheme="postgresql+psycopg2",
        #         username=self.POSTGRES_USER,
        #         password=self.POSTGRES_PASSWORD,
        #         host=self.POSTGRES_SERVER,
        #         port=self.POSTGRES_PORT,
        #         path=self.POSTGRES_DB,
        #     )
        # )
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    ECHO_SQL: bool = False

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:8080",
    ]

    # security settings
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 24


SETTINGS = Settings()
