"""
User related Pydantic schemas
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator


# ============ Skill Schemas ============

class SkillBase(BaseModel):
    """Base skill schema"""
    skill_name: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=50)  # technical, domain, soft
    proficiency_level: Optional[int] = Field(None, ge=1, le=5)
    years_used: Optional[float] = Field(None, ge=0)


class SkillCreate(SkillBase):
    """Schema for creating a skill"""
    pass


class SkillUpdate(BaseModel):
    """Schema for updating a skill"""
    skill_name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=50)
    proficiency_level: Optional[int] = Field(None, ge=1, le=5)
    years_used: Optional[float] = Field(None, ge=0)


class SkillResponse(SkillBase):
    """Skill response schema"""
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Career History Schemas ============

class CareerHistoryBase(BaseModel):
    """Base career history schema"""
    company_name: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=255)
    start_date: datetime
    end_date: Optional[datetime] = None
    is_current: bool = False
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    achievements: Optional[dict] = None
    location: Optional[str] = Field(None, max_length=255)


class CareerHistoryCreate(CareerHistoryBase):
    """Schema for creating career history"""
    pass


class CareerHistoryUpdate(BaseModel):
    """Schema for updating career history"""
    company_name: Optional[str] = Field(None, min_length=1, max_length=255)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    achievements: Optional[dict] = None
    location: Optional[str] = Field(None, max_length=255)


class CareerHistoryResponse(CareerHistoryBase):
    """Career history response schema"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ Education Schemas ============

class EducationBase(BaseModel):
    """Base education schema"""
    institution: str = Field(..., min_length=1, max_length=255)
    degree: Optional[str] = Field(None, max_length=255)
    field_of_study: Optional[str] = Field(None, max_length=255)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    grade: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class EducationCreate(EducationBase):
    """Schema for creating education"""
    pass


class EducationUpdate(BaseModel):
    """Schema for updating education"""
    institution: Optional[str] = Field(None, min_length=1, max_length=255)
    degree: Optional[str] = Field(None, max_length=255)
    field_of_study: Optional[str] = Field(None, max_length=255)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    grade: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class EducationResponse(EducationBase):
    """Education response schema"""
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ============ User Schemas ============

class LocationSchema(BaseModel):
    """Location schema"""
    city: Optional[str] = None
    country: Optional[str] = None


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    location: Optional[LocationSchema] = None
    bio: Optional[str] = None
    linkedin_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=500)
    portfolio_url: Optional[str] = Field(None, max_length=500)


class UserCreate(BaseModel):
    """Schema for creating a user"""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=255)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    full_name: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    location: Optional[LocationSchema] = None
    bio: Optional[str] = None
    linkedin_url: Optional[str] = Field(None, max_length=500)
    github_url: Optional[str] = Field(None, max_length=500)
    portfolio_url: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = Field(None, max_length=500)
    target_roles: Optional[List[str]] = None
    target_salary_min: Optional[int] = Field(None, ge=0)
    target_salary_max: Optional[int] = Field(None, ge=0)
    target_locations: Optional[List[str]] = None


class UserResponse(BaseModel):
    """User response schema (public)"""
    id: UUID
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[dict] = None
    bio: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    avatar_url: Optional[str] = None
    is_email_verified: bool
    target_roles: Optional[List[str]] = None
    target_salary_min: Optional[int] = None
    target_salary_max: Optional[int] = None
    target_locations: Optional[List[str]] = None
    resume_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    """User schema with database fields"""
    hashed_password: str
    is_active: bool
    is_superuser: bool
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None

    class Config:
        from_attributes = True


class UserProfileResponse(UserResponse):
    """User profile response with related data"""
    skills: List[SkillResponse] = []
    career_history: List[CareerHistoryResponse] = []
    education: List[EducationResponse] = []

    class Config:
        from_attributes = True
