from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env once at import time.
# override=False means Docker's env vars (or any pre-set env var) always win.
_env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=_env_path, override=False)

def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. "
            "Set it as an environment variable or in the project-root `.env` file."
        )
    return url


def get_sync_database_url() -> str:
    url = os.getenv("SYNC_DATABASE_URL")

    if not url:
        raise RuntimeError(
            "SYNC_DATABASE_URL is not set. "
            "Set it as an environment variable or in the project-root `.env` file."
        )
    return url


def get_alembic_database_url() -> str:
    url = os.getenv("ALEMBIC_DATABASE_URL")
    if not url:
        raise RuntimeError(
            "ALEMBIC_DATABASE_URL is not set. "
            "Set it as an environment variable or in the project-root `.env` file."
        )
    return url


def get_celery_broker_url() -> str:
    url = os.getenv("CELERY_BROKER_URL")
    if not url:
        raise RuntimeError(
            "CELERY_BROKER_URL is not set. "
            "Set it as an environment variable or in the project-root `.env` file."
        )
    return url

def get_celery_backend_url() -> str:
    url = os.getenv("CELERY_BACKEND_URL")
    if not url:
        raise RuntimeError(
            "CELERY_BACKEND_URL is not set. "
            "Set it as an environment variable or in the project-root `.env` file."
        )
    return url

def get_stripe_secret_key() -> str:
    key = os.getenv("STRIPE_SECRET_KEY")
    if not key:
        raise RuntimeError(
            "STRIPE_SECRET_KEY is not set. "
            "Set it as an environment variable or in the project-root `.env` file."
        )
    return key


def get_gmail_user() -> str:
    user = os.getenv("GMAIL_USER")
    if not user:
        raise RuntimeError(
            "GMAIL_USER is not set. "
            "Set it as an environment variable or in the project-root `.env` file."
        )
    return user

def get_gmail_password() -> str:
    password = os.getenv("GMAIL_PASSWORD")
    if not password:
        raise RuntimeError(
            "GMAIL_PASSWORD is not set. "
            "Set it as an environment variable or in the project-root `.env` file."
        )
    return password

def get_gmail_port() -> int:
    port = os.getenv("GMAIL_PORT")
    if not port:
        raise RuntimeError(
            "GMAIL_PORT is not set. "
            "Set it as an environment variable or in the project-root `.env` file."
        )
    return int(port)

def get_gmail_server() -> str:
    server = os.getenv("GMAIL_SERVER")
    if not server:
        raise RuntimeError(
            "GMAIL_SERVER is not set. "
            "Set it as an environment variable or in the project-root `.env` file."
        )
    return server

def get_domain() -> str:
    domain = os.getenv("DOMAIN")
    if not domain:
        raise RuntimeError(
            "DOMAIN is not set. "
            "Set it as an environment variable or in the project-root `.env` file."
        )
    return domain