# from backendapp.core.config import settings
from app.core.settings import SETTINGS
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class ReadOnlySession(Session):
    def add(self, instance, _warn=True):
        raise RuntimeError("This session is read-only!")

    def add_all(self, instances, _warn=True):
        raise RuntimeError("This session is read-only!")

    def delete(self, instance):
        raise RuntimeError("This session is read-only!")

    def commit(self):
        raise RuntimeError("This session is read-only!")


engine = create_engine(
    SETTINGS.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=40,
    max_overflow=10,
    echo=SETTINGS.ECHO_SQL,
)

ReadOnlySessionLocal = sessionmaker(bind=engine, class_=ReadOnlySession)
SessionLocal = sessionmaker(bind=engine)
