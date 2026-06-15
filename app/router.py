from fastapi import APIRouter, Depends

from app.controllers import AuthController
from app.dependencies import get_controller, get_current_user
from app.dto import (
    CredentialsRequest,
    GuestRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(
    data: CredentialsRequest,
    controller: AuthController = Depends(get_controller),
) -> TokenResponse:
    return await controller.register(data)


@router.post("/guest", response_model=TokenResponse)
async def guest(
    data: GuestRequest,
    controller: AuthController = Depends(get_controller),
) -> TokenResponse:
    return controller.guest(data.name)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: CredentialsRequest,
    controller: AuthController = Depends(get_controller),
) -> TokenResponse:
    return await controller.login(data)


@router.get("/me", response_model=UserResponse)
async def me(
    user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    return user
