from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from helpers.db import PyObjectId
from bson import ObjectId


class UsersTrackedProducts(BaseModel):
    product_link: str = Field(..., min_length=10, max_length=300)



class UsersSchema(BaseModel):
    model_config = ConfigDict(
        title="users",
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True,
        extra="ignore"
    )
    id: Optional[PyObjectId] = Field(alias="_id")
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    tracked_products: Optional[List[UsersTrackedProducts]] = Field(default_factory=list)