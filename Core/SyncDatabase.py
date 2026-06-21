from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from Core.settings import get_sync_database_url

sync_engine = create_engine(get_sync_database_url(), pool_pre_ping=True)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@contextmanager
def get_sync_session() -> Generator[Session, None, None]:
    session = SyncSessionLocal()
    try:
        yield session
    finally:
        session.close()
