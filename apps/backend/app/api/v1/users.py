"""
User API endpoints
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.db.models import User
from app.api.deps import get_current_user
from app.services.user import UserService
from app.schemas.user import (
    UserResponse,
    UserUpdate,
    UserProfileResponse,
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

router = APIRouter()


# ============ Profile ============

@router.get("/me", response_model=UserProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Get current user's full profile with skills, career history, and education
    """
    user_service = UserService(db)
    profile = await user_service.get_user_profile(current_user.id)
    return profile


@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Update current user's profile
    """
    user_service = UserService(db)
    updated_user = await user_service.update_user(current_user, update_data)
    return updated_user


# ============ Skills ============

@router.get("/me/skills", response_model=List[SkillResponse])
async def get_my_skills(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Get current user's skills
    """
    user_service = UserService(db)
    skills = await user_service.get_user_skills(current_user.id)
    return skills


@router.post("/me/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def add_skill(
    skill_data: SkillCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Add a skill to current user's profile
    """
    user_service = UserService(db)
    skill = await user_service.add_skill(current_user.id, skill_data)
    return skill


@router.post("/me/skills/bulk", response_model=List[SkillResponse], status_code=status.HTTP_201_CREATED)
async def add_skills_bulk(
    skills_data: List[SkillCreate],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Add multiple skills at once
    """
    user_service = UserService(db)
    skills = await user_service.bulk_add_skills(current_user.id, skills_data)
    return skills


@router.put("/me/skills/{skill_id}", response_model=SkillResponse)
async def update_skill(
    skill_id: UUID,
    update_data: SkillUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Update a skill
    """
    user_service = UserService(db)
    skill = await user_service.update_skill(skill_id, current_user.id, update_data)
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )
    return skill


@router.delete("/me/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    skill_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Delete a skill
    """
    user_service = UserService(db)
    deleted = await user_service.delete_skill(skill_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found",
        )
    return None


# ============ Career History ============

@router.get("/me/career", response_model=List[CareerHistoryResponse])
async def get_my_career_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Get current user's career history
    """
    user_service = UserService(db)
    career_history = await user_service.get_career_history(current_user.id)
    return career_history


@router.post("/me/career", response_model=CareerHistoryResponse, status_code=status.HTTP_201_CREATED)
async def add_career_history(
    career_data: CareerHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Add career history entry
    """
    user_service = UserService(db)
    career = await user_service.add_career_history(current_user.id, career_data)
    return career


@router.put("/me/career/{career_id}", response_model=CareerHistoryResponse)
async def update_career_history(
    career_id: UUID,
    update_data: CareerHistoryUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Update career history entry
    """
    user_service = UserService(db)
    career = await user_service.update_career_history(
        career_id, current_user.id, update_data
    )
    if career is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career history not found",
        )
    return career


@router.delete("/me/career/{career_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_career_history(
    career_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Delete career history entry
    """
    user_service = UserService(db)
    deleted = await user_service.delete_career_history(career_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Career history not found",
        )
    return None


# ============ Education ============

@router.get("/me/education", response_model=List[EducationResponse])
async def get_my_education(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Get current user's education
    """
    user_service = UserService(db)
    education = await user_service.get_education(current_user.id)
    return education


@router.post("/me/education", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def add_education(
    education_data: EducationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Add education entry
    """
    user_service = UserService(db)
    education = await user_service.add_education(current_user.id, education_data)
    return education


@router.put("/me/education/{education_id}", response_model=EducationResponse)
async def update_education(
    education_id: UUID,
    update_data: EducationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Update education entry
    """
    user_service = UserService(db)
    education = await user_service.update_education(
        education_id, current_user.id, update_data
    )
    if education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education not found",
        )
    return education


@router.delete("/me/education/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(
    education_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Delete education entry
    """
    user_service = UserService(db)
    deleted = await user_service.delete_education(education_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education not found",
        )
    return None


# ============ Resume ============

@router.post("/me/resume", response_model=UserResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    """
    Upload resume file (PDF or DOCX)

    The file will be stored and parsed to extract information
    """
    # Validate file type
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are allowed",
        )

    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 10MB",
        )

    # TODO: Implement file storage (Azure Blob Storage or local)
    # TODO: Implement resume parsing

    # For now, just return the current user
    # In a full implementation, we would:
    # 1. Upload file to storage
    # 2. Parse the file
    # 3. Update user profile with parsed data

    return current_user
