from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ChecklistItem(BaseModel):
    """Checklist item for tracking production steps of content (e.g. Script, Record, Edit, Publish)."""

    __tablename__ = "checklist_items"

    title = Column(String(255), nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    position = Column(Integer, default=0, nullable=False)

    # Foreign Keys
    content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    content = relationship("Content", back_populates="checklists")
