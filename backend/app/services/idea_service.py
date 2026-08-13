import uuid
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.idea_repo import IdeaRepository
from app.schemas.idea import IdeaCreate, IdeaUpdate, QuickCaptureCreate
from app.models.idea import Idea
from app.models.enums import IdeaStatus


class IdeaService:
    """Service handling business rules and transactions for Ideas and Inbox capture."""

    def __init__(self, db: Session):
        self.repo = IdeaRepository(db)

    def quick_capture(self, payload: QuickCaptureCreate) -> Idea:
        """Create a raw unconstrained thought in Inbox with zero required metadata."""
        if not payload.raw_thought.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Raw thought cannot be empty"
            )
        idea_data = {
            "raw_thought": payload.raw_thought.strip(),
            "status": IdeaStatus.RAW
        }
        return self.repo.create(idea_data)

    def create_idea(self, payload: IdeaCreate) -> Idea:
        """Create a full idea with optional title, flair, tags, and prompts."""
        if not payload.raw_thought.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Raw thought cannot be empty"
            )
        idea_data = payload.model_dump(exclude={"tag_ids"}, exclude_unset=True)
        return self.repo.create(idea_data, tag_ids=payload.tag_ids)

    def get_idea(self, idea_id: uuid.UUID) -> Idea:
        """Retrieve idea by ID or raise 404 Not Found."""
        idea = self.repo.get_by_id(idea_id)
        if not idea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Idea with ID '{idea_id}' not found"
            )
        return idea

    def list_ideas(
        self,
        status: Optional[IdeaStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Idea], int]:
        """List ideas with status filters."""
        return self.repo.list_ideas(status=status, skip=skip, limit=limit)

    def update_idea(self, idea_id: uuid.UUID, payload: IdeaUpdate) -> Idea:
        """Update an existing idea and apply business transitions."""
        idea = self.get_idea(idea_id)
        update_data = payload.model_dump(exclude={"tag_ids"}, exclude_unset=True)
        return self.repo.update(idea, update_data, tag_ids=payload.tag_ids)

    def delete_idea(self, idea_id: uuid.UUID) -> None:
        """Delete an idea from database."""
        idea = self.get_idea(idea_id)
        self.repo.delete(idea)
