from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from ..helpers.db import db
from ..helpers.settings import get_settings
from ..users.models import UserModel
from .models import TokenData

environmentConfig = get_settings()

SECRET_KEY = environmentConfig.JWT_SECRET
ALGORITHM = (
    environmentConfig.JWT_ALGORITHM if environmentConfig.JWT_ALGORITHM else "HS256"
)

ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str, db=db) -> TokenData | None:
    user = await db.get_collection("users").find_one({"username": username})
    if not user:
        return None
    user = UserModel(**user)

    if not verify_password(password, user.password):
        return None

    jwt_token_data = TokenData(
        id=str(user.id), username=user.username, email=user.email
    )

    return jwt_token_data


async def validate_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await db.get_collection("users").find_one({"_id": ObjectId(token_data.id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserModel(**user).model_dump(exclude=["password"])
