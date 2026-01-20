# src/m4_auth.py

"""
Milestone 4 – Authentication & JWT Utilities
"""

from datetime import datetime, timedelta
from jose import jwt, JWTError
from src.m4_users import USERS

# JWT configuration
SECRET_KEY = "super-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def authenticate_user(username: str, password: str):
    """
    Validate user credentials.
    """
    user = USERS.get(username)
    if not user:
        return None
    if user["password"] != password:
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a signed JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    Verify JWT token and return payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None