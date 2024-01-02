"""User router for FastAPI."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from prisma.models import User
from prisma.types import (
    UserCreateInput,
)

from ...exceptions import AuthenticationError, InvalidTokenError, UserNotFoundError
from ...services.auth import (
    Token,
)
from ...services.user_service import (
    authenticate_user_and_create_token,
    create_user,
    get_current_active_user,
)

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/sign-in", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """OAuth2 compatible token login, get an access token for future requests.

    Args:
        form_data (OAuth2PasswordRequestForm): The OAuth2 request form data.

    Returns:
        Token: The access token for the authenticated user.

    Raises:
        HTTPException: If authentication fails.
    """
    try:
        return await authenticate_user_and_create_token(
            form_data.username, form_data.password
        )
    except AuthenticationError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
            headers={"WWW-Authenticate": "Bearer"},
        ) from err


@router.post("/user/create", response_model=User)
async def create_user_route(user_data: UserCreateInput) -> User:
    try:
        return await create_user(user_data)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from err


@router.get("/user/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """Retrieve the current authenticated user's details.

    Args:
        current_user (User): The current authenticated user obtained from the token.

    Returns:
        User: The current authenticated user.

    Raises:
        HTTPException: If user is not found or token is invalid.
    """
    try:
        return current_user
    except UserNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from err
    except InvalidTokenError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from err
