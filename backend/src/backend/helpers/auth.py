from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import jwt
from bson import ObjectId
from backend.src.backend.config import get_settings
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordBearer
from helpers.db import db
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from schemas.users import UserSchema

environmentConfig = get_settings()

SECRET_KEY = environmentConfig.JWT_SECRET
ALGORITHM = (
    environmentConfig.JWT_ALGORITHM if environmentConfig.JWT_ALGORITHM else "HS256"
)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


class LoginModel(BaseModel):
    """The Login Model"""

    username: str = Field(
        ...,
        title="Username",
        description="Username of the user... can be an email",
        examples=["amgookool", "amgookool@hotmail.com"],
    )
    password: str = Field(..., title="Password", description="Password of the user")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """The Token Data Model

    This model is used to represent the data contained in the JWT token.

    Attributes:
        id (Optional[str]): The unique identifier of the user.
        username (Optional[str]): The username of the user.
        email (Optional[str]): The email address of the user.
    """

    id: str = Field(..., title="User ID", description="Unique identifier of the user")
    username: str = Field(
        ...,
        title="Username",
        description="Username of the user",
    )
    email: str = Field(
        ...,
        title="Email",
        description="Email address of the user",
    )


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
    user = UserSchema(**user)

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
    return  UserSchema(**user).model_dump(exclude=["password"])


async def get_current_user(
    token_data: Annotated[dict, Depends(validate_token)],
) -> UserSchema:
    """
    Dependency to get the current user from the token.
    This will be used in routes that require authentication.
    """
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_user = UserSchema(**token_data)
    return current_user
