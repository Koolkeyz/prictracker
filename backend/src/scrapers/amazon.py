import re
from typing import Optional, Tuple

from bs4 import BeautifulSoup
from ..helpers.logger import scrapers_logger


class AmazonScraper:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "lxml")

    def get_product_title(self):
        """
        Fetches the product title from the HTML content.

        Returns:
            str: The product title if found, otherwise None.

        Returns:
            None: If the title element is not found in the HTML content.
        """
        title_element = self.soup.find(id="title_feature_div")
        if not title_element:
            return None
        title = title_element.get_text(strip=True)
        return title

    def get_product_seller(self) -> dict | None:
        """
        Fetches the product seller information and where it ships from.

        Returns:
            dict: A dictionary containing 'ships_from' and 'sold_by' information,
                  or None if the information is not available.
        Returns:
            None: If the seller information is not found in the HTML content.
        """
        container_element = self.soup.find(id="desktop_qualifiedBuyBox")
        if not container_element:
            scrapers_logger.warning("Container element not found in the HTML content.")
            return None
        seller_container = container_element.find(id="offer-display-features")
        if not seller_container:
            scrapers_logger.warning("Seller container not found in the HTML content.")
            return None

        ships_from_element = seller_container.find(
            id="fulfillerInfoFeature_feature_div"
        )

        sold_by_element = seller_container.find(id="merchantInfoFeature_feature_div")
        if not ships_from_element:
            scrapers_logger.warning("Ships from element not found in the HTML content.")

        if not sold_by_element:
            scrapers_logger.warning("Sold by element not found in the HTML content.")

        if not ships_from_element and not sold_by_element:
            scrapers_logger.warning("Neither ships from nor sold by elements found in the HTML content.")
            return None

        ships_from_data = ships_from_element.find(
            "span", class_="a-size-small offer-display-feature-text-message"
        ).get_text(strip=True)
        
        print(f"Ships from:", ships_from_data)

        sold_by_data = sold_by_element.find(
            "span", class_="a-size-small offer-display-feature-text-message"
        ).get_text(strip=True)
        
        print(f"Sold by:", sold_by_data)
        return {
            "ships_from": ships_from_data,
            "sold_by": sold_by_data,
        }

    def get_product_price(self) -> float | None:
        """
        Fetches the product price from the HTML content.

        Returns:
            float: The product price if found, otherwise None.
        Returns:
            None: If the price element is not found in the HTML content.
        """
        price_element = self.soup.find("div",id="corePrice_feature_div")
        if not price_element:
            print("Price element not found in the HTML content.")
            return None
        price_text_element = price_element.find("span", class_="a-offscreen")

        if not price_text_element:
            print("Price text element not found in the HTML content.")
            return None
        price_text = price_text_element.get_text(strip=True)
        # Extracting the numeric value from the price text
        price = float(price_text.replace("$", "").replace(",", ""))
        return price

    def get_product_image(self) -> str | None:
        """
        Fetches the product image URL from the HTML content.

        Returns:
            str: The product image URL if found, otherwise None.
        Returns:
            None: If the image element is not found in the HTML content.
        """
        image_container_element = self.soup.find(id="imgTagWrapperId")
        if not image_container_element:
            return None
        image_element = image_container_element.find("img")
        img = image_element.get("src")
        return img if img else None

    def get_product_coupon(self):
        """
        Fetches the product coupon information from the HTML content.

        Returns:
            dict: A dictionary containing 'value' and 'discount_type' if a coupon is found,
                  otherwise None.
        Returns:
            None: If the coupon element is not found in the HTML content.
        """
        coupon_element = self.soup.find(id="promoPriceBlockMessage_feature_div")
        if not coupon_element:
            return None

        coupon_message_element = coupon_element.find(
            "span", class_="a-color-success couponLabelText"
        )
        if not coupon_message_element:
            coupon_message = coupon_element.get_text(strip=True)
        else:
            coupon_message = coupon_message_element.get_text(strip=True)

        parsed_discount = self.parse_discount(coupon_message)

        value, discount_type = parsed_discount if parsed_discount else (None, None)
        if value is None or discount_type is None:
            print("No discount found in the coupon message.")
            return None

        return {
            "value": value,
            "discount_type": discount_type,
        }

    def parse_discount(self, text: str) -> Optional[Tuple[str, str]]:
        """
        Parses the discount value and type from the input string.

        Args:
            text (str): The input string containing the discount.

        Returns:
            A tuple of (value, discount_type) or None if no match is found.
        """
        # Check for fixed amount like "$500"
        fixed_match = re.search(r"\$(\d+(?:\.\d{1,2})?)", text)
        if fixed_match:
            return f"${fixed_match.group(1)}", "fixed"

        # Check for percentage like "10%"
        percent_match = re.search(r"(\d+(?:\.\d{1,2})?)%", text)
        if percent_match:
            return f"{percent_match.group(1)}%", "percentage"

        return None
