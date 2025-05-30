from enum import Enum
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from bson import ObjectId
from helpers.db import PyObjectId


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class UserModel(BaseModel):
    model_config = ConfigDict(
        title="users",
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True,
        extra="allow",
    )
    username: str = Field(
        ..., min_length=3, max_length=50, description="Username of the user"
    )
    email: EmailStr = Field(..., description="Email address of the user")
    first_name: str = Field(
        ..., min_length=2, max_length=50, description="First name of the user"
    )
    last_name: str = Field(
        ..., min_length=2, max_length=50, description="Last name of the user"
    )
    force_password_change: bool = Field(
        default=False, description="Force user to change password on next login"
    )
    role: UserRole = Field(
        UserRole.user, description="Role of the user (admin/user)"
    )


class UserSchema(UserModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    password: str = Field(
        '', min_length=8, max_length=100, description="Hashed password of the user"
    )

class UserUpdateSchema(BaseModel):
    username: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Username of the user"
    )
    email: Optional[EmailStr] = Field(None, description="Email address of the user")
    first_name: Optional[str] = Field(
        None, min_length=2, max_length=50, description="First name of the user"
    )
    last_name: Optional[str] = Field(
        None, min_length=2, max_length=50, description="Last name of the user"
    )
    force_password_change: Optional[bool] = Field(
        None, description="Force user to change password on next login"
    )
