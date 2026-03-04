import logging

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, constr
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import Union

from app.core.config import settings
from app.auth import (
    AuthContext,
    authenticate_user,
    hash_password,
    issue_token,
    optional_active_user,
    require_active_user,
    revoke_token,
)
from app.db.session import get_db
from app.models.models_auth import AuthUser
from app.api.routes import analyze, dialogue

LOGGER = logging.getLogger(__name__)

app = FastAPI(
    title="VR Supermarket AI Service",
    description="API skeleton with JWT authentication and Swagger docs.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# include routers from subpackages
app.include_router(analyze.router)
app.include_router(dialogue.router)


def _jwt_ttl_seconds() -> int:
    return settings.JWT_ACCESS_EXPIRE_MINUTES * 60


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    username: str


class RegisterRequest(BaseModel):
    username: constr(min_length=3, max_length=150)
    password: constr(min_length=8, max_length=128)


@app.post("/auth/login", tags=["Auth"], response_model=TokenResponse, summary="Login and obtain JWT")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = issue_token(db, user)
    return TokenResponse(
        access_token=token,
        expires_in=_jwt_ttl_seconds(),
        username=user.username,
    )


@app.post("/auth/logout", tags=["Auth"], summary="Logout and revoke JWT")
def logout(
    auth: AuthContext = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    revoke_token(db, auth.token_jti)
    return {"status": "logged_out"}


@app.post(
    "/auth/register",
    tags=["Auth"],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
    auth: Union[AuthContext, None] = Depends(optional_active_user),
):
    # stmt_count = select(func.count()).select_from(AuthUser)
    # existing_count = db.scalar(stmt_count) or 0
    # if existing_count > 0 and auth is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Registration is disabled for unauthenticated users.",
    #     )

    stmt = select(AuthUser).where(AuthUser.username == payload.username)
    if db.execute(stmt).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username has been taken.")

    password_bytes = payload.password.encode("utf-8")
    if len(password_bytes) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too long (maximum 72 bytes when UTF-8 encoded).",
        )

    new_user = AuthUser(
        username=payload.username,
        password_hash=hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username}


@app.get("/health", tags=["Health"], summary="Check service health")
def health():
    return {"status": "ok"}
