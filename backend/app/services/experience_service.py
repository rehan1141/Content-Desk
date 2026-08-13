import uuid
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.experience_repo import ExperienceRepository
from app.schemas.experience import ExperienceCreate, ExperienceUpdate
from app.models.experience import Experience


class ExperienceService:
    """Service handling business rules and transactions for Experience entities."""

    def __init__(self, db: Session):
        self.repo = ExperienceRepository(db)

    def create_experience(self, payload: ExperienceCreate) -> Experience:
        """Create a new experience entry in the vault."""
        if not payload.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Experience title cannot be empty"
            )
        exp_data = payload.model_dump(exclude={"tag_ids"}, exclude_unset=True)
        exp_data["title"] = payload.title.strip()
        return self.repo.create(exp_data, tag_ids=payload.tag_ids)

    def get_experience(self, exp_id: uuid.UUID) -> Experience:
        """Retrieve experience by ID or raise 404 Not Found."""
        exp = self.repo.get_by_id(exp_id)
        if not exp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Experience with ID '{exp_id}' not found"
            )
        return exp

    def list_experiences(
        self,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Experience], int]:
        """List experiences with category filters."""
        return self.repo.list_experiences(category=category, skip=skip, limit=limit)

    def update_experience(self, exp_id: uuid.UUID, payload: ExperienceUpdate) -> Experience:
        """Update an existing experience."""
        exp = self.get_experience(exp_id)
        update_data = payload.model_dump(exclude={"tag_ids"}, exclude_unset=True)
        if "title" in update_data and update_data["title"] is not None:
            if not update_data["title"].strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Experience title cannot be empty"
                )
            update_data["title"] = update_data["title"].strip()
        return self.repo.update(exp, update_data, tag_ids=payload.tag_ids)

    def delete_experience(self, exp_id: uuid.UUID) -> None:
        """Delete an experience from database."""
        exp = self.get_experience(exp_id)
        self.repo.delete(exp)
