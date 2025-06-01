from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, status, Body

from ..auth.controller import get_current_user
from ..helpers.db import db
from .models import ProductModel, AmazonProductValidation
from ..users.models import UserModel
from ..helpers.requester import make_request
from ..config.service import get_user_agents, get_proxy_servers
from ..config.models import ConfigModel
from ..scrapers.amazon import AmazonScraper
from ..scrapers.models import ScrapedProductData


router = APIRouter()


@router.post("/validate/amazon")
async def validate_amazon_product(
    product: Annotated[AmazonProductValidation, Body(..., embed=True)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    """
    Validates an Amazon product by checking if the product link is valid by sending a request and initially fetching the data.

    This function also creates the document in the db for tracking the product.
    """
    try:
        user_agents = ConfigModel(**await get_user_agents()).user_agents
        proxy_server = ConfigModel(**await get_proxy_servers()).proxy_servers

        response = make_request(
            url=product.product_url,
            user_agents=user_agents if user_agents else None,
            proxy_servers=proxy_server if len(proxy_server) > 0 else None,
        )
        if response is None or response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid product link or product not found.",
            )

        scraper = AmazonScraper(response.text)

        scraped_data = ScrapedProductData(
            productPrice=scraper.get_product_price(),
            productCoupon=scraper.get_product_coupon(),
            productImage=scraper.get_product_image(),
            productSeller=scraper.get_product_seller(),
            productTitle=scraper.get_product_title(),
        )




        return {
            "message": "Product link is valid.",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/validate/newegg")
async def validate_newegg_product():
    """
    Validates an Newegg product by checking if the product link is valid

    Requires existing user to have role 'admin'.
    """
