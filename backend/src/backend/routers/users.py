from typing import Annotated
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from helpers.db import db
from helpers.auth import get_current_user, get_password_hash
from schemas.users import UserSchema, UserRole
from fastapi import Path
from bson import ObjectId


router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def createUser(
    new_user: UserSchema, current_user: Annotated[UserSchema, Depends(get_current_user)]
):
    """
    Create a new user.
    """
    try:
        if current_user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to create a user",
            )
        if not new_user.username or not new_user.email or not new_user.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username, email, and password are required",
            )
        if len(new_user.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long",
            )

        new_user.password = get_password_hash(new_user.password)
        result = await db.get_collection("users").insert_one(
            new_user.model_dump(by_alias=True, exclude={"id"})
        )
        if not result.acknowledged:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user",
            )
        if result.inserted_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User creation failed, no ID returned",
            )
        return {
            "message": "User created successfully",
            "user_id": str(result.inserted_id),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the user: {str(e)}",
        )


@router.get("/", response_model=list[UserSchema], status_code=status.HTTP_200_OK)
async def getUsers(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    """
    Retrieve a list of all users.
    """
    try:
        if current_user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view users",
            )
        users = await db.get_collection("users").find().to_list(length=None)
        return [UserSchema(**user).model_dump(exclude={"password"}) for user in users]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving users: {str(e)}",
        )


@router.get("/{user_id}", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def getUser(
    user_id: Annotated[str, Path(description="ID of the user to retrieve")],
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    """
    Retrieve a user by ID.
    """
    try:
        if current_user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view this user",
            )
        user = await db.get_collection("users").find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserSchema(**user).model_dump(exclude={"password"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the user: {str(e)}",
        )


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def updateUser(
    user_id: Annotated[str, Path(description="ID of the user to update")],
    updated_user: UserSchema,
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    """
    Update a user's details.
    """
    try:
        if current_user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this user",
            )
        if not updated_user.username or not updated_user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username and email are required",
            )
        if len(updated_user.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long",
            )

        updated_user.password = get_password_hash(updated_user.password)
        result = await db.get_collection("users").update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updated_user.model_dump(by_alias=True, exclude={"id"})},
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or no changes made",
            )
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the user: {str(e)}",
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(
    user_id: Annotated[str, Path(description="ID of the user to delete")],
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    """
    Delete a user by ID.
    """
    try:
        if current_user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this user",
            )
        result = await db.get_collection("users").delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the user: {str(e)}",
        )
