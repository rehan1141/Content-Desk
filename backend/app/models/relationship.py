from sqlalchemy import Column, Enum as SQLEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.enums import LineageType


class ContentRelationship(BaseModel):
    """Model tracking lineage and repurposing relationships between content items."""

    __tablename__ = "content_relationships"

    source_content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"), nullable=False)
    target_content_id = Column(UUID(as_uuid=True), ForeignKey("content.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(
        SQLEnum(LineageType, native_enum=False),
        default=LineageType.REPURPOSED_FROM,
        nullable=False
    )

    # Relationships
    source_content = relationship("Content", foreign_keys=[source_content_id])
    target_content = relationship("Content", foreign_keys=[target_content_id])
