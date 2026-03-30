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
