from datetime import timedelta
from typing import Annotated, Dict
from fastapi.templating import Jinja2Templates
from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Request,
    Response,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from ..mail.mailer import mailer, create_email_message
from ..mail.models import EmailSchema
from ..helpers.logger import auth_logger, log_error, log_request
from ..helpers.settings import get_settings
from ..users.models import UserModel
from .models import PasswordResetChangeModel, PasswordResetModel, Token
from .service import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    create_reset_token,
    get_user_by_email,
    get_user_by_id,
    update_user_password,
    validate_reset_token,
    validate_token,
)

router = APIRouter()
environment = get_settings()


async def get_current_user(
    request: Request,
) -> UserModel:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        token_data = await validate_token(token)
        current_user = UserModel(**token_data)
        return current_user
    except HTTPException as e:
        raise e


@router.post("/token", response_model=Token, tags=["Authentication"])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    request: Request,
) -> Dict[str, str] | Token:
    try:
        auth_logger.info(f"Login attempt for user: {form_data.username}")

        user = await authenticate_user(form_data.username, form_data.password)
        if not user:
            auth_logger.warning(f"Failed login attempt for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expiration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data=user.model_dump(),
            expires_delta=access_token_expiration,
        )
        token_data = Token(access_token=access_token, token_type="bearer")
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True if using HTTPS
            samesite="strict",  # Adjust as needed
        )
        response.set_cookie(
            key="token_type",
            value=token_data.token_type,
            httponly=True,
            secure=False,  # Set to True if using HTTPS
            samesite="strict",  # Adjust as needed
        )
        response.headers["Authorization"] = f"Bearer {access_token}"
        response.headers["Vary"] = "Origin"

        auth_logger.info(f"Successful login for user: {form_data.username}")
        return {
            "access_token": token_data.access_token,
            "token_type": token_data.token_type,
        }
    except HTTPException:
        # Re-raise HTTP exceptions (like 401 Unauthorized)
        raise
    except Exception as e:
        log_error(auth_logger, e, f"Login error for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login",
        )


@router.post("/password-reset", tags=["Authentication"])
async def password_reset(payload: PasswordResetModel):
    """
    Endpoint for password reset.
    This is a placeholder and should be implemented with actual logic.
    """
    try:
        user = await get_user_by_email(payload.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        reset_token = create_reset_token(
            data={
                "email": user.email,
                "id": str(user.id),
            }
        )

        reset_link = f"{environment.APP_HOST}/password-reset/{reset_token}"

        # Implement email sending logic here
        email_schema = EmailSchema(
            email=[user.email],
            body= {
                "resetLink": reset_link,
                "name": f"{user.first_name} {user.last_name}",
            }
        )
        # Render the email body with the data
        
        email_message = create_email_message(
            subject="Password Reset Request",
            recipients=email_schema.model_dump().get("email"),
            body=email_schema.model_dump().get("body"),
        )
        
        await mailer.send_message(message=email_message, template_name="reset-password.html")
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"reset_link": reset_link, "token": reset_token},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/validate-reset-token", tags=["Authentication"])
async def reset_token_validation(
    token: Annotated[str, Body(..., description="Reset token to validate", embed=True)],
):
    """
    Endpoint to validate the reset token.
    This will return the user information if the token is valid.
    """
    try:
        token_data = await validate_reset_token(token)
        user = UserModel(**token_data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "email": user.email,
                "id": str(user.id),
                "username": user.username,
                "token": token,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/password-reset-change", tags=["Authentication"])
async def password_reset_change(
    payload: PasswordResetChangeModel,
):
    """
    Endpoint to change the user's password after validating the reset token.
    """
    try:
        user = await get_user_by_id(payload.id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # Here you would typically hash the new password and update it in the database
        # For demonstration, we assume a function `update_user_password` exists
        updated_user = await update_user_password(
            user=user,
            new_password=payload.new_password,
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Password changed successfully",
                "user": updated_user.model_dump(exclude={"password"}, mode="json"),
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/auth-user", tags=["Authentication"])
async def authenticated_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserModel:
    """
    Endpoint to get the authenticated user.
    This will return the user information based on the token provided.
    """
    try:
        return current_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/logout", tags=["Authentication"])
async def logout():
    """
    Endpoint to log out the user.
    This will clear the authentication cookies.
    """
    try:
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Logged out successfully"},
        )
        response.delete_cookie("access_token", path="/")
        response.delete_cookie("token_type", path="/")
        auth_logger.info("User logged out successfully")
        return response
    except Exception as e:
        log_error(auth_logger, e, "Logout error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during logout",
        )
