from pydantic import BaseModel, Field


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
    access_token: str = Field(..., title="Access Token", description="JWT access token")
    token_type: str = Field(
        "bearer", title="Token Type", description="Type of the token, usually 'bearer'"
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
