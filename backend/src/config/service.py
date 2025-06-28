from ..helpers.db import db, CollectionNames
from .models import ConfigModel
from typing import List, Optional
from bson import ObjectId



async def get_user_agents() -> dict:
    configs_db = await db.get_collection(CollectionNames.CONFIGS).find_one({"_id": "default"})
    if not configs_db:
        raise ValueError("No user agents found")
    configs = ConfigModel(**configs_db)
    return configs.model_dump(exclude={"proxy_servers"})


async def get_proxy_servers() -> dict:
    configs_db = await db.get_collection(CollectionNames.CONFIGS).find_one({"_id": "default"})
    if not configs_db:
        raise ValueError("No proxy servers found")
    configs = ConfigModel(**configs_db)
    return configs.model_dump(exclude={"user_agents"})