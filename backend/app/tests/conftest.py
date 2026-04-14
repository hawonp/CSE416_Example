from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session, close_all_sessions, sessionmaker
from sqlalchemy.pool import StaticPool

from app.apis.dependencies import (
    get_current_superuser_id,
    get_current_user_id,
    get_db,
    get_readonly_db,
)
from app.apis.v1.login import router as login_router
from app.apis.v1.quotes import router as quote_router
from app.apis.v1.users import router as user_router
from app.core.settings import SETTINGS
from app.models.base import Base
from app.tests.fixtures import FIXED_USER_ID, quote_dataset, user_dataset, users_dataset
from app.utils.security import create_access_token

#####################
# IMPORTED FIXTURES #
#####################
_ = [user_dataset]
_ = [quote_dataset]
_ = [users_dataset]

app = FastAPI()

app.include_router(login_router, prefix=SETTINGS.API_V1_STR)
app.include_router(user_router, prefix=SETTINGS.API_V1_STR)
app.include_router(quote_router, prefix=SETTINGS.API_V1_STR)


#####################
# DATABASE FIXTURES #
#####################
@compiles(ARRAY, "sqlite")
def compile_array(element, compiler, **kwargs):
    """
    Custom compilation for ARRAY type in SQLite.
    """
    return "TEXT"


# @pytest.fixture(scope="session")
@pytest.fixture(scope="function")
def engine() -> Generator[Engine, None, None]:
    """
    Create a single in-memory SQLite engine for the test session,
    then dispose it after tests complete.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},  # Allow cross-thread usage
        poolclass=StaticPool,  # Use static pool to share the same connection
    )

    # Enable foreign key constraints in SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # create tables using engine
    with engine.begin() as conn:
        # conn.run_sync(base.UUIDAuditBase.metadata.create_all)
        Base.metadata.create_all(conn)
    yield engine
    close_all_sessions()
    engine.dispose()


@pytest.fixture(scope="function")
def session_factory(engine) -> sessionmaker[Session]:
    """
    Provide an sessionmaker bound to the in-memory engine.
    """
    return sessionmaker(
        bind=engine,
        class_=Session,
        expire_on_commit=False,
    )


# 3. Provide a session per test
@pytest.fixture(scope="function")
def fake_db_session(
    session_factory: sessionmaker[Session],
) -> Generator[Session, None, None]:
    """
    Yields a fresh Session bound to an in-memory SQLite DB.
    """
    with session_factory() as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


#######################
# TEST CLIENT FIXTURE #
#######################
@pytest.fixture(scope="function")
def test_client(
    fake_db_session: Session,
) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = lambda: fake_db_session
    app.dependency_overrides[get_readonly_db] = lambda: fake_db_session
    app.dependency_overrides[get_current_user_id] = lambda: FIXED_USER_ID

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def test_protected_client(
    fake_db_session: Session,
) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = lambda: fake_db_session
    app.dependency_overrides[get_readonly_db] = lambda: fake_db_session
    app.dependency_overrides[get_current_superuser_id] = lambda: FIXED_USER_ID

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def login_token() -> dict:
    token = create_access_token({"sub": str(FIXED_USER_ID)})
    return {"Authorization": f"Bearer {token}"}
