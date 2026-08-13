import uuid
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc
from app.models.experience import Experience
from app.models.tag import Tag


class ExperienceRepository:
    """Repository handling database operations for Experience entities."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, exp_data: dict, tag_ids: Optional[List[uuid.UUID]] = None) -> Experience:
        """Create a new experience entity in database."""
        exp = Experience(**exp_data)
        if tag_ids:
            tags = self.db.scalars(select(Tag).where(Tag.id.in_(tag_ids))).all()
            exp.tags.extend(tags)
        self.db.add(exp)
        self.db.commit()
        self.db.refresh(exp)
        return exp

    def get_by_id(self, exp_id: uuid.UUID) -> Optional[Experience]:
        """Fetch single experience by UUID primary key."""
        return self.db.scalar(select(Experience).where(Experience.id == exp_id))

    def list_experiences(
        self,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[Experience], int]:
        """List experiences with optional category filtering and pagination."""
        query = select(Experience)
        count_query = select(func.count(Experience.id))

        if category:
            query = query.where(Experience.category == category)
            count_query = count_query.where(Experience.category == category)

        total = self.db.scalar(count_query) or 0
        items = self.db.scalars(
            query.order_by(desc(Experience.created_at)).offset(skip).limit(limit)
        ).all()
        return list(items), total

    def update(self, exp: Experience, update_data: dict, tag_ids: Optional[List[uuid.UUID]] = None) -> Experience:
        """Update fields on an existing experience entity."""
        for field, value in update_data.items():
            if value is not None:
                setattr(exp, field, value)

        if tag_ids is not None:
            tags = self.db.scalars(select(Tag).where(Tag.id.in_(tag_ids))).all()
            exp.tags = list(tags)

        self.db.commit()
        self.db.refresh(exp)
        return exp

    def delete(self, exp: Experience) -> None:
        """Permanently delete an experience from database."""
        self.db.delete(exp)
        self.db.commit()
