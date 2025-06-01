import requests
from requests import Response
from typing import List, Optional
import random


def make_request(
    url: str,
    user_agents: Optional[List[str]] = None,
    proxy_servers: Optional[List[str]] = None,
    timeout: int = 60,
) -> Optional[Response]:
    """
    Makes a GET request to the specified URL and returns the response.

    Args:
        url (str): The URL to make the request to.

    Returns:
        requests.Response: The response object from the GET request.
    """
    try:
        headers = {
            "User-Agent": (
                random.choice(user_agents)
                if user_agents
                else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.5",
        }

        if proxy_servers:
            proxy = {
                "http": random.choice(proxy_servers),
                "https": random.choice(proxy_servers),
            }
        else:
            proxy = None

        response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
        response.raise_for_status()  # Raise an error for bad responses
        return response
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
