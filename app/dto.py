from pydantic import BaseModel, Field


class CredentialsRequest(BaseModel):
    login: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=4, max_length=128)


class GuestRequest(BaseModel):
    name: str = Field(min_length=2, max_length=64)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    login: str


class UserResponse(BaseModel):
    user_id: str
    login: str
