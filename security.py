import jwt
from typing import Annotated
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models import User
from settings import settings


oauth2_scheme = OAuth2PasswordBearer("login")

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


# JWT TOKEN


def create_access_token(sub: dict) -> str:
    to_encode = sub.copy()

    expire_at = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode["exp"] = expire_at

    access_token = jwt.encode(
        to_encode, settings.SECRET_KEY.get_secret_value(), algorithm=settings.ALGORITHM
    )

    return access_token
