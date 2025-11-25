"""
Security utilities for authentication
JWT token handling and password hashing
"""

from datetime import datetime, timedelta
from typing import Any, Optional
import uuid
import secrets

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token types
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_access_token(
    subject: str | uuid.UUID,
    expires_delta: Optional[timedelta] = None,
    extra_claims: Optional[dict] = None,
) -> str:
    """
    Create a JWT access token

    Args:
        subject: The subject (usually user ID)
        expires_delta: Token expiration time delta
        extra_claims: Additional claims to include in the token

    Returns:
        Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": ACCESS_TOKEN_TYPE,
        "jti": str(uuid.uuid4()),  # JWT ID for tracking
    }

    if extra_claims:
        to_encode.update(extra_claims)

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: str | uuid.UUID,
    expires_delta: Optional[timedelta] = None,
) -> tuple[str, datetime]:
    """
    Create a JWT refresh token

    Args:
        subject: The subject (usually user ID)
        expires_delta: Token expiration time delta

    Returns:
        Tuple of (encoded JWT token string, expiration datetime)
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Refresh tokens last 7 days by default
        expire = datetime.utcnow() + timedelta(days=7)

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": REFRESH_TOKEN_TYPE,
        "jti": str(uuid.uuid4()),
    }

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt, expire


def verify_token(token: str, token_type: str = ACCESS_TOKEN_TYPE) -> Optional[dict]:
    """
    Verify and decode a JWT token

    Args:
        token: The JWT token string
        token_type: Expected token type (access or refresh)

    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )

        # Verify token type
        if payload.get("type") != token_type:
            return None

        return payload
    except JWTError:
        return None


def verify_access_token(token: str) -> Optional[dict]:
    """Verify an access token"""
    return verify_token(token, ACCESS_TOKEN_TYPE)


def verify_refresh_token(token: str) -> Optional[dict]:
    """Verify a refresh token"""
    return verify_token(token, REFRESH_TOKEN_TYPE)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_verification_token() -> str:
    """Generate a random verification token for email verification"""
    return secrets.token_urlsafe(32)


def generate_password_reset_token() -> str:
    """Generate a random token for password reset"""
    return secrets.token_urlsafe(32)
