from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from Core.settings import get_database_url

Base = declarative_base()

_engine = None
_session_local = None


def _get_engine_and_session():
    global _engine, _session_local
    if _engine is None:
        _engine = create_engine(get_database_url())
        _session_local = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _engine, _session_local


def get_db() -> Generator:
    _, SessionLocal = _get_engine_and_session()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
