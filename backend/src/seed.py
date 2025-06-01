from .auth.service import get_password_hash
from .helpers.db import db
from .users.models import UserModel
from .helpers.db import db


async def create_user():
    user = UserModel(
        username="adrian.gookool",
        email="amgookool@hotmail.com",
        password=get_password_hash("PriceTracker"),
        first_name="Adrian",
        last_name="Gookool",
        role="admin",
    )
    # Insert the user into the database
    result = await db.get_collection("users").insert_one(
        user.model_dump(by_alias=True, exclude={"id"})
    )
    if result.acknowledged:
        print(f"User created with ID: {result.inserted_id}")
    else:
        print("Failed to create user.")


async def seed_user_agents():
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
    result = await db.get_collection("configs").insert_one(
        {"_id": "default", "userAgents": user_agents}
    )
    if result.acknowledged:
        print("User agents seeded successfully.")
    else:
        print("Failed to seed user agents.")


async def seed_database():
    print("Seeding database...")
    # await create_user()
    await seed_user_agents()
    print("Database seeding completed.")


if __name__ == "__main__":
    import asyncio

    # Run the seed function
    asyncio.run(seed_database())
