import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def _get_str(name: str, default: str = "") -> str:
    value = os.getenv(name)
    return value.strip() if value is not None else default


def _get_optional_str(name: str) -> Optional[str]:
    value = os.getenv(name)
    if value is None:
        return None
    value = value.strip()
    return value or None


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    # PostgreSQL URL (set via .env or docker-compose)
    DB_URL: str = _get_str("DB_URL", "postgresql://postgres:postgres@localhost:5432/vr_supermarket_db")
    JWT_SECRET_KEY: Optional[str] = _get_optional_str("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = _get_str("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_EXPIRE_MINUTES: int = _get_int("JWT_ACCESS_EXPIRE_MINUTES", 60)
    PORT: int = _get_int("PORT", 8080)


settings = Settings()
