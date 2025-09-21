from datetime import datetime, timedelta
from jose import JWTError, jwt

from core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

"""
This module provides functions for creating and decoding JWT access tokens.
"""
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT access token.

    Args:
        data: The data to encode in the token.
        expires_delta: The expiration time for the token.

    Returns:
        The encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """
    Decodes a JWT access token.

    Args:
        token: The token to decode.

    Returns:
        The decoded token, or None if the token is invalid.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= datetime.utcnow().timestamp() else None
    except JWTError:
        return None