from config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

environmentConfig = get_settings()
client = AsyncIOMotorClient(environmentConfig.MONGO_URI)
db = client[environmentConfig.MONGO_DB]

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")