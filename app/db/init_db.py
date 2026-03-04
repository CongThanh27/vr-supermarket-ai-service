#!/usr/bin/env python3
"""Initialize database schema"""

import sys
from app.db.session import Base, get_engine
from app.models.models_auth import AuthUser, AuthToken

if __name__ == "__main__":
    try:
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
        print("[ok] Database schema created successfully")
    except Exception as e:
        print(f"[error] Failed to create database schema: {e}", file=sys.stderr)
        sys.exit(1)
