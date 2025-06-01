from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List
from bson import ObjectId
from ..helpers.db import PyObjectId


class ConfigModel(BaseModel):
    """Configuration Model for the application settings"""

    model_config = ConfigDict(
        title="config",
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        populate_by_name=True,
        extra="allow",
    )

    id: Optional[PyObjectId] = Field(
        default='default',
        alias="_id",
        description="Unique identifier for the configuration",
    )
    
    user_agents: Optional[List[str]] = Field(
        default_factory=list,
        description="List of user agents to be used for requests",
        alias="userAgents",
    )
    proxy_servers: Optional[List[str]] = Field(
        default_factory=list,
        description="List of proxy servers to be used for requests",
        alias="proxyServers",
    )