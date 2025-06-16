from .db import db, CollectionNames
from ..users.models import UserModel, UserRole
from ..auth.service import get_password_hash
from .settings import get_settings


environment = get_settings()
collections = CollectionNames()


async def check_if_user_agents_exist() -> bool:
    """
    Check if user agents exist in the database.

    Returns:
        bool: True if user agents exist, False otherwise.
    """
    try:
        user_agents = await db.get_collection(collections.CONFIGS).find_one({"_id": "default"})
        # ensure that user agents list is not none and the array length is greater than 0
        if user_agents is None:
            return False
        if "userAgents" not in user_agents or not isinstance(
            user_agents["userAgents"], list
        ):
            return False
        if len(user_agents["userAgents"]) == 0:
            return False
        return True  # Return True if all checks pass
    except Exception as e:
        print(f"Error checking user agents existence: {e}")
        return False


async def add_user_agents():
    try:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edge/44.18363.8131",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.10 Safari/605.1.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Trailer/93.3.8652.5",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.1958",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.3",
        ]
        # Insert user agents into the database
        result = await db.get_collection(collections.CONFIGS).insert_one(
            {"_id": "default", "userAgents": user_agents}
        )
        if not result.acknowledged:
            raise Exception("Failed to add user agents")
        print(f"User agents added successfully with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error adding user agents: {e}")
        raise e


async def check_if_user_exists(username: str) -> bool:
    """
    Check if a user with the given username exists in the database.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    try:
        user = await db.get_collection(collections.USERS).find_one(
            {"username": username}
        )
        return user is not None
    except Exception as e:
        print(f"Error checking user existence: {e}")
        return False

async def create_user():
    try:
        user = UserModel(
            role=UserRole.admin,
            username=environment.ADMIN_USERNAME,
            password=get_password_hash(environment.ADMIN_PASSWORD),
            email=environment.ADMIN_EMAIL,
            firstName="Admin",
            lastName="User",
        )

        result = await db.get_collection(collections.USERS).insert_one(
            user.model_dump(by_alias=True, exclude={"id"})
        )

        if not result.acknowledged:
            raise Exception("Failed to create admin user")

        print(f"Admin user created with ID: {result.inserted_id}")

    except Exception as e:
        print(f"Error creating admin user: {e}")
        raise e
