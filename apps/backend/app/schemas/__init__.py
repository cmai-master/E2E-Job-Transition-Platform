"""
Pydantic Schemas
"""

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserInDB,
    SkillCreate,
    SkillUpdate,
    SkillResponse,
    CareerHistoryCreate,
    CareerHistoryUpdate,
    CareerHistoryResponse,
    EducationCreate,
    EducationUpdate,
    EducationResponse,
)
from app.schemas.auth import (
    Token,
    TokenPayload,
    LoginRequest,
    SignupRequest,
    RefreshTokenRequest,
    PasswordChangeRequest,
    PasswordResetRequest,
    OAuthRequest,
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserInDB",
    "SkillCreate",
    "SkillUpdate",
    "SkillResponse",
    "CareerHistoryCreate",
    "CareerHistoryUpdate",
    "CareerHistoryResponse",
    "EducationCreate",
    "EducationUpdate",
    "EducationResponse",
    # Auth schemas
    "Token",
    "TokenPayload",
    "LoginRequest",
    "SignupRequest",
    "RefreshTokenRequest",
    "PasswordChangeRequest",
    "PasswordResetRequest",
    "OAuthRequest",
]
