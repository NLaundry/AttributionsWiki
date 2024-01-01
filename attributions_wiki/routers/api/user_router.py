"""User router for FastAPI."""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from prisma.models import User
from prisma.types import (
    UserCreateInput,
)

from ...db import db
from ...services.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,  #type: ignore
    get_current_active_user,
    get_password_hash,
)

router = APIRouter(
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    # Recall that username is a required field by ouath ... their username is their email
    # This is going to cause some WTFs
    # TODO: how do I indicate that username and email are the same thing?
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@router.post("/user/create/")
async def create_user(user_data: UserCreateInput) -> User:
    """Create a new user.

    Args: user_data: UserCreateInput
    Returns: User
    """
    if (user_data["password"] != user_data["rpassword"]):
        raise HTTPException(
        status_code=403,
        detail="Passwords do not match",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_data["password"] = get_password_hash(user_data["password"])
    new_user: User = await db.user.create(user_data)
    return new_user
