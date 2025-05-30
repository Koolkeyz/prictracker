from backend.config import get_settings
from bson import ObjectId
from pymongo import AsyncMongoClient
from typing import Annotated
from pydantic import BeforeValidator

environmentConfig = get_settings()
mongo_uri = environmentConfig.MONGO_URI.strip()

client = AsyncMongoClient(mongo_uri,)
db = client[environmentConfig.MONGO_DB]

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]
