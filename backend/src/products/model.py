from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from helpers.db import PyObjectId
from bson import ObjectId
from datetime import datetime
from enum import Enum


class ProductPlatformEnum(str, Enum):
    amazon = "amazon"
    newegg = "newegg"
    ebay = "ebay"


class ProductModel(BaseModel):
    model_config = ConfigDict(
        title="product",
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True,
        extra="ignore",
    )
    id: Optional[PyObjectId] = Field(
        default=None,
        alias="_id",
        description="Unique identifier for the product",
    )
    platform: ProductPlatformEnum = Field(
        ..., description="Platform where the product is listed"
    )
    product_link: str = Field(
        ..., min_length=10, description="Link to the product page"
    )
    product_name: str = Field(
        ..., min_length=3, max_length=250, description="Name of the product"
    )
    price: float = Field(
        ..., gt=0, decimal_places=2, description="Price of the product"
    )
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp when the product was added",
    )
