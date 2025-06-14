import re
from typing import Optional, Tuple

from bs4 import BeautifulSoup


class NeweggScraper:

    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "lxml")

    def get_product_title(self) -> str | None:
        """
        Fetches the product title from the HTML content for Newegg products.

        Returns:
            str: The product title if found, otherwise None.
        """
        # Try to find an <h1> with class containing 'product-title'
        title_element = self.soup.find(
            "h1", class_=lambda c: c and "product-title" in c
        )
        if not title_element:
            # Fallback: use the first <h1> tag
            title_element = self.soup.find("h1")
        if not title_element:
            return None
        title = title_element.get_text(strip=True)
        return title

    def get_product_seller(self) -> dict | None:
        """
        Fetches the product seller information and where it ships from for Newegg products.

        Returns:
            dict: A dictionary containing 'ships_from' and 'sold_by' information, or None if not found.
        """
        seller_info = {"ships_from": None, "sold_by": None}
        # FInd element with class 'product-seller-box'
        seller_element = self.soup.find(
            "div", class_=lambda c: c and "product-seller-box" in c
        )
        sold_by_element = seller_element.find(
            "div", class_="product-seller-sold-by"
        )
        ships_from_element = seller_element.find(
            "div", class_="product-seller-box-shhips"
        )
        if sold_by_element:
            strong_element = sold_by_element.find("strong")
            if strong_element:
                seller_info["sold_by"] = strong_element.get_text(strip=True)
        if ships_from_element:
            strong_element = ships_from_element.find("a").find("strong")
            if strong_element:
                seller_info["ships_from"] = strong_element.get_text(strip=True)

        return seller_info

    def get_product_price(self) -> float | None:
        """
        Fetches the product price from the HTML content.

        Returns:
            float: The product price if found, otherwise None.
        Returns:
            None: If the price element is not found in the HTML content.
        """
        price_container_element = self.soup.find("div",class_="price-new-right")
        if not price_container_element:
            return None
        price_element = price_container_element.find("div", class_="price-current")
        if not price_element:
            return None
        price_text = price_element.get_text(strip=True)
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
        image_parent_container_element = self.soup.find(id="side-product-gallery")
        if not image_parent_container_element:
            return None
        image_carousel_element = image_parent_container_element.find(
            id="side-swiper-container"
        )
        if not image_carousel_element:
            return None
        # Assuming the image is within an <img> tag inside the carousel element
        image_container_elements = image_carousel_element.find_all("img")
        if not image_container_elements:
            return None

        # iterate through the images and get all the image urls
        image_urls = []
        for image_element in image_container_elements:
            img_url = image_element.get("src")
            if img_url:
                image_urls.append(img_url)
        if not image_urls:
            return None
        return image_urls[0]  # Return the first image URL found

    def get_product_coupon(self):
        """
        Fetches the product coupon information from the HTML content.

        Returns:
            dict: A dictionary containing 'value' and 'discount_type' if a coupon is found,
                  otherwise None.
        Returns:
            None: If the coupon element is not found in the HTML content.
        """
        return None

    def parse_discount(self, text: str) -> Optional[Tuple[str, str]]:
        """
        Parses the discount value and type from the input string.

        Args:
            text (str): The input string containing the discount.

        Returns:
            A tuple of (value, discount_type) or None if no match is found.
        """
        # Check for fixed amount like "$500"
        return None
