"""
User Service
Business logic for user management
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.db.models import User, Skill, CareerHistory, Education
from app.schemas.user import (
    UserUpdate,
    SkillCreate,
    SkillUpdate,
    CareerHistoryCreate,
    CareerHistoryUpdate,
    EducationCreate,
    EducationUpdate,
)


class UserService:
    """User service"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_profile(self, user_id: UUID) -> Optional[User]:
        """Get user with all related data"""
        result = await self.db.execute(
            select(User)
            .options(
                selectinload(User.skills),
                selectinload(User.career_history),
                selectinload(User.education),
            )
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def update_user(self, user: User, update_data: UserUpdate) -> User:
        """
        Update user profile

        Args:
            user: User object
            update_data: Update data

        Returns:
            Updated user object
        """
        update_dict = update_data.model_dump(exclude_unset=True)

        # Handle location separately if provided
        if "location" in update_dict and update_dict["location"]:
            update_dict["location"] = update_dict["location"]

        for field, value in update_dict.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    # ============ Skills ============

    async def get_user_skills(self, user_id: UUID) -> List[Skill]:
        """Get all skills for a user"""
        result = await self.db.execute(
            select(Skill).where(Skill.user_id == user_id).order_by(Skill.created_at)
        )
        return list(result.scalars().all())

    async def add_skill(self, user_id: UUID, skill_data: SkillCreate) -> Skill:
        """Add a skill to user"""
        skill = Skill(
            user_id=user_id,
            **skill_data.model_dump(),
        )
        self.db.add(skill)
        await self.db.commit()
        await self.db.refresh(skill)
        return skill

    async def update_skill(
        self, skill_id: UUID, user_id: UUID, update_data: SkillUpdate
    ) -> Optional[Skill]:
        """Update a skill"""
        result = await self.db.execute(
            select(Skill).where(Skill.id == skill_id, Skill.user_id == user_id)
        )
        skill = result.scalar_one_or_none()

        if skill is None:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(skill, field, value)

        await self.db.commit()
        await self.db.refresh(skill)
        return skill

    async def delete_skill(self, skill_id: UUID, user_id: UUID) -> bool:
        """Delete a skill"""
        result = await self.db.execute(
            select(Skill).where(Skill.id == skill_id, Skill.user_id == user_id)
        )
        skill = result.scalar_one_or_none()

        if skill is None:
            return False

        await self.db.delete(skill)
        await self.db.commit()
        return True

    async def bulk_add_skills(
        self, user_id: UUID, skills_data: List[SkillCreate]
    ) -> List[Skill]:
        """Add multiple skills at once"""
        skills = [
            Skill(user_id=user_id, **skill_data.model_dump())
            for skill_data in skills_data
        ]
        self.db.add_all(skills)
        await self.db.commit()

        # Refresh all skills
        for skill in skills:
            await self.db.refresh(skill)

        return skills

    # ============ Career History ============

    async def get_career_history(self, user_id: UUID) -> List[CareerHistory]:
        """Get career history for a user"""
        result = await self.db.execute(
            select(CareerHistory)
            .where(CareerHistory.user_id == user_id)
            .order_by(CareerHistory.start_date.desc())
        )
        return list(result.scalars().all())

    async def add_career_history(
        self, user_id: UUID, career_data: CareerHistoryCreate
    ) -> CareerHistory:
        """Add career history entry"""
        career = CareerHistory(
            user_id=user_id,
            **career_data.model_dump(),
        )
        self.db.add(career)
        await self.db.commit()
        await self.db.refresh(career)
        return career

    async def update_career_history(
        self, career_id: UUID, user_id: UUID, update_data: CareerHistoryUpdate
    ) -> Optional[CareerHistory]:
        """Update career history entry"""
        result = await self.db.execute(
            select(CareerHistory).where(
                CareerHistory.id == career_id, CareerHistory.user_id == user_id
            )
        )
        career = result.scalar_one_or_none()

        if career is None:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(career, field, value)

        await self.db.commit()
        await self.db.refresh(career)
        return career

    async def delete_career_history(self, career_id: UUID, user_id: UUID) -> bool:
        """Delete career history entry"""
        result = await self.db.execute(
            select(CareerHistory).where(
                CareerHistory.id == career_id, CareerHistory.user_id == user_id
            )
        )
        career = result.scalar_one_or_none()

        if career is None:
            return False

        await self.db.delete(career)
        await self.db.commit()
        return True

    # ============ Education ============

    async def get_education(self, user_id: UUID) -> List[Education]:
        """Get education for a user"""
        result = await self.db.execute(
            select(Education)
            .where(Education.user_id == user_id)
            .order_by(Education.start_date.desc())
        )
        return list(result.scalars().all())

    async def add_education(
        self, user_id: UUID, education_data: EducationCreate
    ) -> Education:
        """Add education entry"""
        education = Education(
            user_id=user_id,
            **education_data.model_dump(),
        )
        self.db.add(education)
        await self.db.commit()
        await self.db.refresh(education)
        return education

    async def update_education(
        self, education_id: UUID, user_id: UUID, update_data: EducationUpdate
    ) -> Optional[Education]:
        """Update education entry"""
        result = await self.db.execute(
            select(Education).where(
                Education.id == education_id, Education.user_id == user_id
            )
        )
        education = result.scalar_one_or_none()

        if education is None:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(education, field, value)

        await self.db.commit()
        await self.db.refresh(education)
        return education

    async def delete_education(self, education_id: UUID, user_id: UUID) -> bool:
        """Delete education entry"""
        result = await self.db.execute(
            select(Education).where(
                Education.id == education_id, Education.user_id == user_id
            )
        )
        education = result.scalar_one_or_none()

        if education is None:
            return False

        await self.db.delete(education)
        await self.db.commit()
        return True

    # ============ Resume ============

    async def update_resume_url(self, user: User, resume_url: str) -> User:
        """Update user's resume URL"""
        user.resume_url = resume_url
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_resume_parsed_data(
        self, user: User, parsed_data: dict
    ) -> User:
        """Update user's resume parsed data"""
        user.resume_parsed_data = parsed_data
        await self.db.commit()
        await self.db.refresh(user)
        return user
