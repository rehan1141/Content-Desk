from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.tag import experience_tags


class Experience(BaseModel):
    """First-class Experience entity representing personal stories, lessons, and milestones."""

    __tablename__ = "experiences"

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    takeaway = Column(Text, nullable=True)
    category = Column(String(50), nullable=True, default="Personal")

    # Foreign Keys
    flair_id = Column(UUID(as_uuid=True), ForeignKey("flairs.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    flair = relationship("Flair")
    tags = relationship("Tag", secondary=experience_tags, back_populates="experiences")
