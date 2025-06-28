from enum import Enum
from typing import  Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field



class ScrapedProductSeller(BaseModel):
    ships_from: Optional[str] = Field(
        None, description="Where the product is shipping from", alias="shipsFrom"
    )
    sold_by: Optional[str] = Field(
        None, description="Who is selling the product", alias="soldBy"
    )


class ProductCouponType(str, Enum):
    fixed = "fixed"
    percentage = "percent"


class ScrapedProductCoupon(BaseModel):
    value: int = Field(
        ...,
        description="The value of the coupon. Can be a percentage or a fixed amount",
    )
    discount_type: ProductCouponType = Field(
        ..., description="Type of coupon. 'fixed' or 'percentage'"
    )


class ScrapedProductData(BaseModel):
    model_config = ConfigDict(
        title="scraped Product Model",
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=False,
        extra="ignore",
    )
    product_title: str = Field(
        ..., description="Title of the scraped product", alias="productTitle"
    )
    product_image: str = Field(
        ..., description="Image UR of the scraped product", alias="productImage"
    )
    product_seller: Optional[ScrapedProductSeller] = Field(
        None,
        description="Data on who is selling product and where product is shipping",
        alias="productSeller",
    )
    product_price: Optional[float] = Field(None, description="The price of the product", alias="productPrice")
    product_coupon: Optional[ScrapedProductCoupon] = Field(
        None, description="Coupon information for the product", alias="productCoupon"
    )
