from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status

router = APIRouter()


@router.post("/create", status_code=status.HTTP_200_OK)
async def createUser():
    """
    Create a new user.
    """

    try:
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the user: {str(e)}",
        )
