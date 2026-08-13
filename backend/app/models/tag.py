from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.db.session import Base

# Association Tables for Many-to-Many relationships
idea_tags = Table(
    "idea_tags",
    Base.metadata,
    Column("idea_id", UUID(as_uuid=True), ForeignKey("ideas.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

content_tags = Table(
    "content_tags",
    Base.metadata,
    Column("content_id", UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

experience_tags = Table(
    "experience_tags",
    Base.metadata,
    Column("experience_id", UUID(as_uuid=True), ForeignKey("experiences.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(BaseModel):
    """Tag entity for categorizing ideas, content items, and experiences."""

    __tablename__ = "tags"

    name = Column(String(50), unique=True, nullable=False, index=True)
    color = Column(String(20), nullable=True, default="#6366f1")

    # Relationships
    ideas = relationship("Idea", secondary=idea_tags, back_populates="tags")
    contents = relationship("Content", secondary=content_tags, back_populates="tags")
    experiences = relationship("Experience", secondary=experience_tags, back_populates="tags")
