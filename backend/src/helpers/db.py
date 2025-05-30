from typing import Annotated

from bson import ObjectId
from pydantic import BeforeValidator
from pymongo import AsyncMongoClient

from .settings import get_settings


environmentConfig = get_settings()
mongo_uri = environmentConfig.MONGO_URI.strip()

client = AsyncMongoClient(
    mongo_uri,
)
db = client[environmentConfig.MONGO_DB]

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]
