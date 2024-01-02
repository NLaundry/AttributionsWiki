from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException

from prisma.errors import MissingRequiredValueError, PrismaError, RecordNotFoundError
from prisma.models import User
from prisma.types import (
    UserCreateInput,
    UserWhereUniqueInput,
)

from ..db import db
from ..exceptions import AuthenticationError, UserNotFoundError
from .auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    extract_username_from_token,
    oauth2_scheme,
    pwd_context,
    validate_token,
)


# TODO: type this
# made these internal methods ... front end should not have access to these
def _verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.

    Args:
        plain_password: Plain text password.
        hashed_password: Hashed password.

    Returns:
        bool: True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def _get_password_hash(password: str) -> str:
    """Generate a password hash.

    Args:
        password: Plain text password.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)


# TODO: move to user_service
async def _get_user_by_username(username: str) -> User | None:
    user_obj: UserWhereUniqueInput = {"email": username}
    try:
        user: User | None = await db.user.find_unique_or_raise(user_obj)
    except RecordNotFoundError as err:
        raise UserNotFoundError("User not found") from err
    else:
        return user


# TODO: move to user_service
async def _authenticate_user(username: str, password: str) -> User | None:
    """Authenticate a user based on username and password.

    Args:
        username: Username of the user.
        password: Password of the user.

    Returns:
        User or None: Authenticated user object or None if authentication fails.
    """
    user: User | None = await _get_user_by_username(username)
    if not user or not _verify_password(password, user.password):
        return None
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Retrieve the current user based on the verified token.

    Args:
        token: A string representation of the user's OAuth2 token.

    Returns:
        User: The current authenticated user.

    Raises:
        UserNotFoundError: If the user does not exist.
    """
    await validate_token(token)
    username = await extract_username_from_token(token)
    user = await _get_user_by_username(username)
    if not user:
        raise UserNotFoundError("User not found")
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """Get the current active user.

    Args:
        current_user: User object from dependency.

    Returns:
        User: The current active user.

    Raises:
        HTTPException: If user is disabled or inactive.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def authenticate_user_and_create_token(
    username: str, password: str
) -> dict[str, str]:
    """Authenticate a user and create an access token.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        dict: A dictionary containing the access token and the token type.

    Raises:
        AuthenticationError: If authentication fails.
    """
    user: User | None = await _authenticate_user(username, password)
    if not user:
        raise AuthenticationError("Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def create_user(user_data: UserCreateInput) -> User:
    """Create a new user in the system.

    Args:
        user_data: UserCreateInput - The data for creating the user.

    Returns:
        User: The newly created user object.

    Raises:
        ValueError: If user creation fails.
    """
    user_data["password"] = _get_password_hash(user_data["password"])
    try:
        new_user: User = await db.user.create(user_data)
        return new_user
    # TODO: More specific error handling
    except MissingRequiredValueError as err:
        # Log the exception or handle it as needed
        raise ValueError("Failed to create user") from err
    except PrismaError as err:
        # Log the exception or handle it as needed
        raise Exception("Failed to create user") from err
