import uuid
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc
from app.models.idea import Idea
from app.models.enums import IdeaStatus
from app.models.tag import Tag


class IdeaRepository:
    """Repository handling database operations for Idea entities."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, idea_data: dict, tag_ids: Optional[List[uuid.UUID]] = None) -> Idea:
        """Create a new idea entity in database."""
        idea = Idea(**idea_data)
        if tag_ids:
            tags = self.db.scalars(select(Tag).where(Tag.id.in_(tag_ids))).all()
            idea.tags.extend(tags)
        self.db.add(idea)
        self.db.commit()
        self.db.refresh(idea)
        return idea

    def get_by_id(self, idea_id: uuid.UUID) -> Optional[Idea]:
        """Fetch single idea by UUID primary key."""
        return self.db.scalar(select(Idea).where(Idea.id == idea_id))

    def list_ideas(
        self,
        status: Optional[IdeaStatus] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Idea], int]:
        """List ideas filtered by status with total count and pagination."""
        query = select(Idea)
        count_query = select(func.count(Idea.id))

        if status:
            query = query.where(Idea.status == status)
            count_query = count_query.where(Idea.status == status)

        total = self.db.scalar(count_query) or 0
        ideas = self.db.scalars(
            query.order_by(desc(Idea.created_at)).offset(skip).limit(limit)
        ).all()
        return list(ideas), total

    def update(self, idea: Idea, update_data: dict, tag_ids: Optional[List[uuid.UUID]] = None) -> Idea:
        """Update fields on an existing idea entity."""
        for field, value in update_data.items():
            if value is not None:
                setattr(idea, field, value)

        if tag_ids is not None:
            tags = self.db.scalars(select(Tag).where(Tag.id.in_(tag_ids))).all()
            idea.tags = list(tags)

        self.db.commit()
        self.db.refresh(idea)
        return idea

    def delete(self, idea: Idea) -> None:
        """Permanently delete an idea from database."""
        self.db.delete(idea)
        self.db.commit()
