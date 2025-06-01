from fastapi import APIRouter, Depends, HTTPException, status
from ..helpers.db import db
from .models import ConfigModel
from .service import get_user_agents as get_user_agents_service
from .service import get_proxy_servers as get_proxy_servers_service

router = APIRouter()


@router.get(
    "/user-agents",
    tags=["Configuration"],
    response_model=ConfigModel,
    response_model_exclude={"proxy_servers"},
)
async def get_user_agents():
    """
    Retrieve the list of user agents.
    """
    try:
        configs_dict = await get_user_agents_service()
        if not configs_dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user agents found",
            )
        configs = ConfigModel(**configs_dict)
        return configs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving user agents: {str(e)}",
        )


@router.put(
    "/user-agents/update", status_code=status.HTTP_200_OK, tags=["Configuration"]
)
async def update_user_agents(user_agents: list[str]):
    """
    Update the list of user agents.
    """
    try:
        if not user_agents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User agents list cannot be empty",
            )
        result = await db.get_collection("user_agents").delete_many({})
        if result.deleted_count > 0:
            await db.get_collection("user_agents").insert_many(
                [{"user_agent": ua} for ua in user_agents]
            )
        return {"message": "User agents updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating user agents: {str(e)}",
        )


@router.get(
    "/proxy-servers",
    tags=["Configuration"],
    response_model=ConfigModel,
    response_model_exclude={"user_agents"},
)
async def get_proxy_servers():
    """
    Retrieve the list of proxy servers.
    """
    try:
        configs_dict = await get_proxy_servers_service()
        if not configs_dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No proxy servers found",
            )
        configs = ConfigModel(**configs_dict)
        return configs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving proxy servers: {str(e)}",
        )
