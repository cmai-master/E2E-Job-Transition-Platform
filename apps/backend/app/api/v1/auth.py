"""
Authentication API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.db.models import User
from app.api.deps import get_current_user
from app.services.auth import AuthService
from app.schemas.auth import (
    Token,
    LoginRequest,
    SignupRequest,
    RefreshTokenRequest,
    PasswordChangeRequest,
    OAuthRequest,
)
from app.schemas.user import UserResponse

router = APIRouter()


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Register a new user

    - **email**: User email (must be unique)
    - **password**: Password (min 8 chars, must include uppercase, lowercase, digit)
    - **full_name**: Optional full name
    """
    auth_service = AuthService(db)

    # Check if user already exists
    existing_user = await auth_service.get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create user
    user = await auth_service.create_user(
        email=request.email,
        password=request.password,
        full_name=request.full_name,
    )

    # Create tokens
    tokens = await auth_service.create_tokens(user)

    # Update last login
    await auth_service.update_last_login(user)

    return tokens


@router.post("/login", response_model=Token)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Login with email and password

    Returns access and refresh tokens
    """
    auth_service = AuthService(db)

    # Authenticate user
    user = await auth_service.authenticate_user(request.email, request.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    # Create tokens
    tokens = await auth_service.create_tokens(user)

    # Update last login
    await auth_service.update_last_login(user)

    return tokens


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Refresh access token using refresh token

    The old refresh token is revoked and a new one is issued
    """
    auth_service = AuthService(db)

    tokens = await auth_service.refresh_tokens(request.refresh_token)
    if tokens is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return tokens


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Logout by revoking the refresh token
    """
    auth_service = AuthService(db)
    await auth_service.revoke_refresh_token(request.refresh_token)
    return None


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Logout from all devices by revoking all refresh tokens
    """
    auth_service = AuthService(db)
    await auth_service.revoke_all_user_tokens(current_user.id)
    return None


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    request: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Change user password

    All refresh tokens will be revoked (force re-login on all devices)
    """
    auth_service = AuthService(db)

    success = await auth_service.change_password(
        user=current_user,
        current_password=request.current_password,
        new_password=request.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password",
        )

    return None


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    Get current authenticated user information
    """
    return current_user


@router.post("/oauth", response_model=Token)
async def oauth_login(
    request: OAuthRequest,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Login or register with OAuth provider (Google or LinkedIn)

    - **provider**: OAuth provider ("google" or "linkedin")
    - **access_token**: OAuth provider access token
    """
    auth_service = AuthService(db)

    # Verify OAuth token and get user info
    if request.provider == "google":
        oauth_info = await auth_service.verify_google_token(request.access_token)
    elif request.provider == "linkedin":
        oauth_info = await auth_service.verify_linkedin_token(request.access_token)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider: {request.provider}",
        )

    if oauth_info is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OAuth token",
        )

    # Get or create user
    user, is_new = await auth_service.get_or_create_oauth_user(oauth_info)

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    # Create tokens
    tokens = await auth_service.create_tokens(user)

    # Update last login
    await auth_service.update_last_login(user)

    return tokens
