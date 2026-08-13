from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Flair(BaseModel):
    """Reddit-style primary flair entity (Opinion, Story, Hot Take, Educational, etc.)."""

    __tablename__ = "flairs"

    name = Column(String(50), unique=True, nullable=False, index=True)
    color = Column(String(20), nullable=True, default="#8b5cf6")
    description = Column(String(255), nullable=True)

    # Relationships
    ideas = relationship("Idea", back_populates="flair")
    contents = relationship("Content", back_populates="flair")
