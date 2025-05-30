from bson import ObjectId
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from helpers.db import db



router = APIRouter()


@router.get("/user-agents", tags=["Configuration"])
async def get_user_agents():
    """
    Retrieve the list of user agents.
    """
    try:
        configs = await db.get_collection("configs").find_one({"_id": "default"})
        if not configs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user agents found",
            )
        
        return {"user_agents": configs.get("user_agents")}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving user agents: {str(e)}",
        )
    

@router.put("/user-agents/update", status_code=status.HTTP_200_OK, tags=["Configuration"])
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