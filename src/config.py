"""Central place to load environment variables and access secrets."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Resolve .env relative to the project root so it works from any working directory.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def require_env(name: str) -> str:
    """Return the value of an environment variable or raise if it is missing/empty."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value
