from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..auth.controller import get_current_user
from ..helpers.db import db, CollectionNames
from ..helpers.logger import products_logger, log_error, log_database_operation
from .models import ProductModel, ProductValidation
from ..users.models import UserModel
from ..helpers.requester import make_request
from ..config.service import get_user_agents, get_proxy_servers
from ..config.models import ConfigModel
from ..scrapers.amazon import AmazonScraper
from ..scrapers.newegg import NeweggScraper
from ..scrapers.ebay import EbayScraper
from ..scrapers.models import (
    ScrapedProductData,
    ScrapedProductSeller,
    ScrapedProductCoupon,
)


router = APIRouter()


@router.get("/")
async def get_user_products(
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    """
    Retrieves all products for the current user.

    Requires existing user to have role 'admin'.
    """
    products_logger.info(f"Fetching products for user: {current_user.username}")
    try:
        # products = await db.get_collection("products").find()
        # products = await db.products.find({"user_id": ObjectId(current_user.id)}).to_list(length=None)
        # log_database_operation(products_logger, "get_user_products", current_user.id, "products")
        # return {"products": [ProductModel(**product).model_dump() for product in products]}
        return JSONResponse(
            content={"message": "Products fetched successfully.", "products": []},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        log_error(
            products_logger,
            e,
            f"Error fetching products for user: {current_user.username}",
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while fetching products",
        )


@router.post("/validate/amazon")
async def validate_amazon_product(
    product: Annotated[ProductValidation, Body(..., embed=False)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    """
    Validates an Amazon product by checking if the product link is valid by sending a request and initially fetching the data.

    This function also creates the document in the db for tracking the product.
    """
    try:
        products_logger.info(
            f"Validating Amazon product for user: {current_user.username}"
        )
        products_logger.debug(f"Product URL: {product.product_url}")

        user_agents = ConfigModel(**await get_user_agents()).user_agents
        proxy_server = ConfigModel(**await get_proxy_servers()).proxy_servers

        products_logger.info("Making request to product URL")
        response = make_request(
            url=product.product_url,
            user_agents=user_agents if user_agents else None,
            proxy_servers=proxy_server if len(proxy_server) > 0 else None,
        )

        if response is None or response.status_code != 200:
            products_logger.warning(
                f"Invalid product link - Status: {response.status_code if response else 'None'}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid product link or product not found.",
            )

        products_logger.info("Scraping product data")
        scraper = AmazonScraper(response.text)
        seller_info = scraper.get_product_seller()
        if not seller_info:
            products_logger.warning("No seller information found in the product page.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product link is valid but no seller information found.",
            )
        product_seller = ScrapedProductSeller(
            shipsFrom=seller_info.get("ships_from"), soldBy=seller_info.get("sold_by")
        )

        coupon_info = scraper.get_product_coupon()
        if not coupon_info:
            product_coupon = None
        else:
            product_coupon = ScrapedProductCoupon(
                value=coupon_info.get("value"),
                discount_type=coupon_info.get("discount_type"),
            )

        scraped_data = ScrapedProductData(
            productPrice=scraper.get_product_price(),
            productImage=scraper.get_product_image(),
            productTitle=scraper.get_product_title(),
            productCoupon=product_coupon,
            productSeller=product_seller,
        )

        products_logger.info(
            f"Successfully scraped product: {scraped_data.product_title}"
        )
        products_logger.debug(f"Product price: {scraped_data.product_price}")

        return {
            "message": "Product link is valid.",
            "product_url": product.product_url,
            "product_data": scraped_data.model_dump(by_alias=False),
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        log_error(
            products_logger,
            e,
            f"Error validating Amazon product for user: {current_user.username}",
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during product validation",
        )


@router.post("/validate/newegg")
async def validate_newegg_product(
    product: Annotated[ProductValidation, Body(..., embed=False)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    """
    Validates an Newegg product by checking if the product link is valid

    Requires existing user to have role 'admin'.
    """
    try:
        products_logger.info(
            f"Validating Newegg product for user: {current_user.username}"
        )
        products_logger.debug(f"Product URL: {product.product_url}")

        user_agents = ConfigModel(**await get_user_agents()).user_agents
        proxy_server = ConfigModel(**await get_proxy_servers()).proxy_servers
        products_logger.info("Making request to product URL")

        response = make_request(
            product.product_url,
            user_agents=user_agents if user_agents else None,
            proxy_servers=proxy_server if len(proxy_server) > 0 else None,
        )

        if response is None or response.status_code != 200:
            products_logger.warning(
                f"Invalid product link - Status: {response.status_code if response else 'None'}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid product link or product not found.",
            )

        products_logger.info("Scraping product data")
        scraper = NeweggScraper(response.text)

        seller_info = scraper.get_product_seller()
        if not seller_info:
            products_logger.warning("No seller information found in the product page.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product link is valid but no seller information found.",
            )
        product_seller = ScrapedProductSeller(
            shipsFrom=seller_info.get("ships_from"), soldBy=seller_info.get("sold_by")
        )

        coupon_info = scraper.get_product_coupon()
        if not coupon_info:
            product_coupon = None
        else:
            product_coupon = ScrapedProductCoupon(
                value=coupon_info.get("value"),
                discount_type=coupon_info.get("discount_type"),
            )

        scraped_data = ScrapedProductData(
            productTitle=scraper.get_product_title(),
            productPrice=scraper.get_product_price(),
            productImage=scraper.get_product_image(),
            productSeller= product_seller,
            productCoupon= product_coupon,
        )

        products_logger.info(
            f"Successfully scraped product: {scraped_data.product_title}"
        )
        products_logger.debug(f"Product price: {scraped_data.product_price}")

        return {
            "message": "Product link is valid.",
            "product_url": product.product_url,
            "product_data": scraped_data.model_dump(),
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        log_error(
            products_logger,
            e,
            f"Error validating Newegg product for user: {current_user.username}",
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during product validation",
        )


@router.post("/validate/ebay")
async def validate_ebay_product(
    product: Annotated[ProductValidation, Body(..., embed=False)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    """
    Validates an eBay product by checking if the product link is valid.

    This function currently does not implement any specific validation logic.
    """
    try:

        products_logger.info(
            f"Validating eBay product for user: {current_user.username}"
        )
        products_logger.debug(f"Product URL: {product.product_url}")

        user_agents = ConfigModel(**await get_user_agents()).user_agents
        proxy_server = ConfigModel(**await get_proxy_servers()).proxy_servers
        products_logger.info("Making request to product URL")

        response = make_request(
            product.product_url,
            user_agents=user_agents if user_agents else None,
            proxy_servers=proxy_server if len(proxy_server) > 0 else None,
        )

        if response is None or response.status_code != 200:
            products_logger.warning(
                f"Invalid product link - Status: {response.status_code if response else 'None'}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid product link or product not found.",
            )

        products_logger.info("Scraping product data")
        scraper = EbayScraper(response.text)
        
        seller_info = scraper.get_product_seller()
        if not seller_info:
            products_logger.warning("No seller information found in the product page.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product link is valid but no seller information found.",
            )
        product_seller = ScrapedProductSeller(
            shipsFrom=seller_info.get("ships_from"), soldBy=seller_info.get("sold_by")
        )
        
        product_coupon = scraper.get_product_coupon()
        if not product_coupon:
            product_coupon = None
        else:
            product_coupon = ScrapedProductCoupon(
                value=product_coupon.get("value"),
                discount_type=product_coupon.get("discount_type"),
            )

        scraped_data = ScrapedProductData(
            productTitle=scraper.get_product_title(),
            productPrice=scraper.get_product_price(),
            productImage=scraper.get_product_image(),
            productSeller=product_seller,
            productCoupon=product_coupon,
        )

        return {
            "message": "Product link is valid.",
            "product_url": product.product_url,
            "product_data": scraped_data.model_dump(),
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        log_error(
            products_logger,
            e,
            f"Error validating eBay product for user: {current_user.username}",
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during product validation",
        )


@router.post("/add")
async def add_product(
    product: Annotated[ProductModel, Body(..., embed=False)],
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    """
    Adds a new product to the user's product list.

    Requires existing user to have role 'admin'.
    """
    try:
        products_logger.info(f"Adding product for user: {current_user.username}")
        products_logger.debug(f"Product data: {product.model_dump()}")

        # Validate the product data
        if not product.product_link:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product URL is required.",
            )

        # Create a new product document
        product_data = jsonable_encoder(product)
        product_data["user_id"] = ObjectId(current_user.id)

        # Insert the product into the database
        result = await db.get_collection(CollectionNames.PRODUCTS).insert_one(product_data)
        log_database_operation(
            products_logger, "add_product", current_user.id, "products"
        )

        return JSONResponse(
            content={
                "message": "Product added successfully.",
                "product_id": str(result.inserted_id),
            },
            status_code=status.HTTP_201_CREATED,
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        log_error(
            products_logger,
            e,
            f"Error adding product for user: {current_user.username}",
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while adding product",
)