"""Authentication module for the API."""
from datetime import datetime, timedelta
from typing import Annotated

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from ..exceptions import InvalidTokenError, UsernameNotFoundError

# Load the .env file
load_dotenv()

# TODO: these need o go in a .env file ... probably
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/sign-in")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    """Token model representing an OAuth2 token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data model for token payload."""

    username: str | None = None


def create_access_token(
    data: dict[str, str], expires_delta: timedelta | None = None
) -> Annotated[str, "encoded_jwt"]:
    """Create an access token with optional expiry.

    Args:
        data: The payload data for the token.
        expires_delta: Expiry time delta.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def validate_token(token: str) -> bool:
    """Validate an OAuth2 token.

    Args:
        token: A string representation of the user's OAuth2 token.

    Returns:
        bool: True if the token is valid.

    Raises:
        InvalidTokenError: If the token is invalid.
    """
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except JWTError as err:
        raise InvalidTokenError("Could not validate credentials") from err


async def extract_username_from_token(token: str) -> str:
    """Extract the username from the token payload.

    Args:
        token: A string representation of the user's OAuth2 token.

    Returns:
        str: The username extracted from the token.

    Raises:
        UsernameNotFoundError: If the username is not present in the token payload.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if not username:
        raise UsernameNotFoundError("Token does not contain a valid username")
    return username
