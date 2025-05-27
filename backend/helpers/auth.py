import jwt
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from config import get_settings
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.security import OAuth2PasswordBearer

environmentConfig = get_settings()

SECRET_KEY = environmentConfig.JWT_SECRET
ALGORITHM = environmentConfig.JWT_ALGORITHM if environmentConfig.JWT_ALGORITHM else "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    """The Token Data Model"""
    id: Optional[str]
    username: Optional[str]
    email: Optional[str]


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)