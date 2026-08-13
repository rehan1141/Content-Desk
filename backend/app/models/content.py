from sqlalchemy import Column, String, Text, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import PlatformType, ContentTypeEnum, ContentStatus
from app.models.tag import content_tags


class Content(BaseModel):
    """Content entity representing actual platform-specific content items (videos, posts, reels)."""

    __tablename__ = "content"

    title = Column(String(255), nullable=False)
    body_script = Column(Text, nullable=True)
    platform = Column(
        SQLEnum(PlatformType, native_enum=False),
        nullable=False,
        index=True
    )
    content_type = Column(
        SQLEnum(ContentTypeEnum, native_enum=False),
        nullable=False,
        index=True
    )
    status = Column(
        SQLEnum(ContentStatus, native_enum=False),
        default=ContentStatus.DRAFT,
        nullable=False,
        index=True
    )

    # Foreign Keys
    parent_idea_id = Column(UUID(as_uuid=True), ForeignKey("ideas.id", ondelete="SET NULL"), nullable=True)
    flair_id = Column(UUID(as_uuid=True), ForeignKey("flairs.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    parent_idea = relationship("Idea", back_populates="contents")
    flair = relationship("Flair", back_populates="contents")
    tags = relationship("Tag", secondary=content_tags, back_populates="contents")
    checklists = relationship("ChecklistItem", back_populates="content", cascade="all, delete-orphan")
