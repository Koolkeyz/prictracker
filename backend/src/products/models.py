from datetime import datetime
from enum import Enum
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..helpers.db import PyObjectId
from ..scrapers.models import ScrapedProductSeller, ScrapedProductCoupon


class ProductPlatformEnum(str, Enum):
    amazon = "amazon"
    newegg = "newegg"
    ebay = "ebay"


class ProductTracking(BaseModel):
    price: float = Field(..., gt=0, description="Current price of the product", ge=0.01)
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the product was scraped",
    )
    seller: Optional[ScrapedProductSeller] = Field(
        default=None,
        description="Seller of the product. Contains where the package is 'ships_from' and who the product is 'sold_by'",
    )
    coupon: Optional[ScrapedProductCoupon] = Field(
        default=None,
        description="If the product has a coupon (discount) on the product"
    )


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
    user_id: str = Field(
        ...,
        description="The Id of the user who this product belongs too",
        alias="userId",
    )
    platform: ProductPlatformEnum = Field(
        ...,
        description="Platform where the product is listed",
    )
    product_link: str = Field(
        ..., min_length=10, description="Link to the product page", alias="productLink"
    )
    product_name: str = Field(
        ...,
        min_length=3,
        max_length=250,
        description="Name of the product",
        alias="productName",
    )
    product_image: Optional[str] = Field(
        default=None, description="URL of the product image", alias="productImage"
    )
    product_tracking: List[ProductTracking] = Field(
        default_factory=list,
        description="List of price tracking records",
        alias="productTracking",
    )
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp when the product was added",
        alias="createdAt",
    )


class AmazonProductValidation(BaseModel):
    product_url: str = Field(
        ..., min_length=10, description="Amazon product URL", alias="productUrl"
    )
