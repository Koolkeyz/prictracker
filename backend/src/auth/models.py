from pydantic import BaseModel, Field, EmailStr


class LoginModel(BaseModel):
    """The Login Model"""

    username: str = Field(
        ...,
        title="Username",
        description="Username of the user... can be an email",
        examples=["amgookool", "amgookool@hotmail.com"],
    )
    password: str = Field(..., title="Password", description="Password of the user")


class Token(BaseModel):
    access_token: str = Field(..., title="Access Token", description="JWT access token", alias="access_token")
    token_type: str = Field(
        "bearer", title="Token Type", description="Type of the token, usually 'bearer'",
        alias="token_type",
    )


class TokenData(BaseModel):
    """The Token Data Model

    This model is used to represent the data contained in the JWT token.

    Attributes:
        id (Optional[str]): The unique identifier of the user.
        username (Optional[str]): The username of the user.
        email (Optional[str]): The email address of the user.
    """

    id: str = Field(..., title="User ID", description="Unique identifier of the user")
    username: str = Field(
        ...,
        title="Username",
        description="Username of the user",
    )
    email: str = Field(
        ...,
        title="Email",
        description="Email address of the user",
    )

class ResetTokenData(BaseModel):
    """The Reset Token Data Model

    This model is used to represent the data contained in the password reset token.

    Attributes:
        email (str): The email address of the user.
        id (str): The unique identifier of the user.
    """

    email: str = Field(..., title="Email", description="Email address of the user")
    id: str = Field(..., title="User ID", description="Unique identifier of the user")


class PasswordResetModel(BaseModel):
    """The Password Reset Model

    This model is used to represent the data required for resetting a user's password.

    Attributes:
        email (str): The email address of the user requesting the password reset.
        new_password (str): The new password to be set for the user.
    """

    email: EmailStr = Field(
        ...,
        title="Email",
        description="Email address of the user requesting the password reset",
    )


class PasswordResetChangeModel(BaseModel):
    """The Password Change Model

    This model is used to represent the data required for changing a user's password.

    Attributes:
        old_password (str): The current password of the user.
        new_password (str): The new password to be set for the user.
    """
    id: str = Field(
        ...,
        title="User ID",
        description="Unique identifier of the user",
    )
    email: EmailStr = Field(
        ...,
        title="Email",
        description="Email address of the user requesting the password change",
    )
    new_password: str = Field(
        ...,
        title="New Password",
        description="New password to be set for the user",
        alias="newPassword",
    )
