"""
Authentication Service
Business logic for user authentication
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple
from uuid import UUID
import httpx

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.models import User, RefreshToken
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    get_password_hash,
    verify_password,
    generate_verification_token,
)
from app.schemas.auth import Token, OAuthUserInfo


class AuthService:
    """Authentication service"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user by email and password

        Args:
            email: User email
            password: User password

        Returns:
            User object if authentication successful, None otherwise
        """
        result = await self.db.execute(
            select(User).where(User.email == email.lower())
        )
        user = result.scalar_one_or_none()

        if user is None:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    async def create_user(
        self,
        email: str,
        password: str,
        full_name: Optional[str] = None,
    ) -> User:
        """
        Create a new user

        Args:
            email: User email
            password: User password
            full_name: User full name

        Returns:
            Created user object
        """
        user = User(
            email=email.lower(),
            hashed_password=get_password_hash(password),
            full_name=full_name,
            email_verification_token=generate_verification_token(),
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.db.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_tokens(self, user: User) -> Token:
        """
        Create access and refresh tokens for user

        Args:
            user: User object

        Returns:
            Token object with access and refresh tokens
        """
        # Create access token
        access_token = create_access_token(
            subject=user.id,
            extra_claims={"email": user.email},
        )

        # Create refresh token
        refresh_token, expires_at = create_refresh_token(subject=user.id)

        # Store refresh token in database
        db_refresh_token = RefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=expires_at,
        )
        self.db.add(db_refresh_token)
        await self.db.commit()

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def refresh_tokens(self, refresh_token: str) -> Optional[Token]:
        """
        Refresh access token using refresh token

        Args:
            refresh_token: Refresh token string

        Returns:
            New token object or None if invalid
        """
        # Verify token
        payload = verify_refresh_token(refresh_token)
        if payload is None:
            return None

        user_id = payload.get("sub")
        if user_id is None:
            return None

        # Check if refresh token exists and is not revoked
        result = await self.db.execute(
            select(RefreshToken).where(
                and_(
                    RefreshToken.token == refresh_token,
                    RefreshToken.is_revoked == False,
                    RefreshToken.expires_at > datetime.utcnow(),
                )
            )
        )
        db_token = result.scalar_one_or_none()

        if db_token is None:
            return None

        # Revoke old refresh token
        db_token.is_revoked = True
        db_token.revoked_at = datetime.utcnow()

        # Get user
        user = await self.get_user_by_id(UUID(user_id))
        if user is None or not user.is_active:
            return None

        # Create new tokens
        return await self.create_tokens(user)

    async def revoke_refresh_token(self, refresh_token: str) -> bool:
        """
        Revoke a refresh token (logout)

        Args:
            refresh_token: Refresh token string

        Returns:
            True if revoked, False otherwise
        """
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token == refresh_token)
        )
        db_token = result.scalar_one_or_none()

        if db_token is None:
            return False

        db_token.is_revoked = True
        db_token.revoked_at = datetime.utcnow()
        await self.db.commit()

        return True

    async def revoke_all_user_tokens(self, user_id: UUID) -> int:
        """
        Revoke all refresh tokens for a user

        Args:
            user_id: User ID

        Returns:
            Number of tokens revoked
        """
        result = await self.db.execute(
            select(RefreshToken).where(
                and_(
                    RefreshToken.user_id == user_id,
                    RefreshToken.is_revoked == False,
                )
            )
        )
        tokens = result.scalars().all()

        count = 0
        for token in tokens:
            token.is_revoked = True
            token.revoked_at = datetime.utcnow()
            count += 1

        await self.db.commit()
        return count

    async def update_last_login(self, user: User) -> None:
        """Update user's last login timestamp"""
        user.last_login_at = datetime.utcnow()
        await self.db.commit()

    async def change_password(
        self, user: User, current_password: str, new_password: str
    ) -> bool:
        """
        Change user password

        Args:
            user: User object
            current_password: Current password
            new_password: New password

        Returns:
            True if changed, False if current password is wrong
        """
        if not verify_password(current_password, user.hashed_password):
            return False

        user.hashed_password = get_password_hash(new_password)
        await self.db.commit()

        # Revoke all refresh tokens (force re-login)
        await self.revoke_all_user_tokens(user.id)

        return True

    # OAuth methods
    async def get_or_create_oauth_user(
        self, oauth_info: OAuthUserInfo
    ) -> Tuple[User, bool]:
        """
        Get existing OAuth user or create new one

        Args:
            oauth_info: OAuth user info

        Returns:
            Tuple of (User, is_new_user)
        """
        # Check if user exists with this OAuth ID
        result = await self.db.execute(
            select(User).where(
                and_(
                    User.oauth_provider == oauth_info.provider,
                    User.oauth_id == oauth_info.oauth_id,
                )
            )
        )
        user = result.scalar_one_or_none()

        if user:
            return user, False

        # Check if user exists with this email
        result = await self.db.execute(
            select(User).where(User.email == oauth_info.email.lower())
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            # Link OAuth to existing account
            existing_user.oauth_provider = oauth_info.provider
            existing_user.oauth_id = oauth_info.oauth_id
            if oauth_info.avatar_url and not existing_user.avatar_url:
                existing_user.avatar_url = oauth_info.avatar_url
            await self.db.commit()
            await self.db.refresh(existing_user)
            return existing_user, False

        # Create new user
        user = User(
            email=oauth_info.email.lower(),
            hashed_password=get_password_hash(generate_verification_token()),  # Random password
            full_name=oauth_info.full_name,
            avatar_url=oauth_info.avatar_url,
            oauth_provider=oauth_info.provider,
            oauth_id=oauth_info.oauth_id,
            is_email_verified=True,  # OAuth emails are verified
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user, True

    async def verify_google_token(self, access_token: str) -> Optional[OAuthUserInfo]:
        """
        Verify Google OAuth token and get user info

        Args:
            access_token: Google access token

        Returns:
            OAuthUserInfo if valid, None otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://www.googleapis.com/oauth2/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                if response.status_code != 200:
                    return None

                data = response.json()
                return OAuthUserInfo(
                    provider="google",
                    oauth_id=data["id"],
                    email=data["email"],
                    full_name=data.get("name"),
                    avatar_url=data.get("picture"),
                )
        except Exception:
            return None

    async def verify_linkedin_token(self, access_token: str) -> Optional[OAuthUserInfo]:
        """
        Verify LinkedIn OAuth token and get user info

        Args:
            access_token: LinkedIn access token

        Returns:
            OAuthUserInfo if valid, None otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                # Get profile info
                profile_response = await client.get(
                    "https://api.linkedin.com/v2/userinfo",
                    headers={"Authorization": f"Bearer {access_token}"},
                )
                if profile_response.status_code != 200:
                    return None

                profile_data = profile_response.json()

                return OAuthUserInfo(
                    provider="linkedin",
                    oauth_id=profile_data["sub"],
                    email=profile_data["email"],
                    full_name=profile_data.get("name"),
                    avatar_url=profile_data.get("picture"),
                )
        except Exception:
            return None
