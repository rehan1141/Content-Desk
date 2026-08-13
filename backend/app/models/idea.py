from sqlalchemy import Column, String, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import IdeaStatus
from app.models.tag import idea_tags


class Idea(BaseModel):
    """Core Idea entity representing raw thoughts and developing content concepts."""

    __tablename__ = "ideas"

    title = Column(String(255), nullable=True)
    raw_thought = Column(Text, nullable=False)
    development_notes = Column(Text, nullable=True)
    status = Column(
        SQLEnum(IdeaStatus, native_enum=False),
        default=IdeaStatus.RAW,
        nullable=False,
        index=True
    )

    # Thinking aids / development prompts
    why_prompt = Column(Text, nullable=True)
    what_happened_prompt = Column(Text, nullable=True)
    actual_point_prompt = Column(Text, nullable=True)

    # Foreign Keys
    flair_id = Column(UUID(as_uuid=True), ForeignKey("flairs.id", ondelete="SET NULL"), nullable=True)
    experience_id = Column(UUID(as_uuid=True), ForeignKey("experiences.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    flair = relationship("Flair", back_populates="ideas")
    experience = relationship("Experience")
    tags = relationship("Tag", secondary=idea_tags, back_populates="ideas")
    contents = relationship("Content", back_populates="parent_idea", cascade="all, delete-orphan")
