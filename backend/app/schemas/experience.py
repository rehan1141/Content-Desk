import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.tag import TagResponse
from app.schemas.flair import FlairResponse


class ExperienceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    takeaway: Optional[str] = None
    category: Optional[str] = "Personal"
    flair_id: Optional[uuid.UUID] = None
    tag_ids: Optional[List[uuid.UUID]] = []


class ExperienceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    takeaway: Optional[str] = None
    category: Optional[str] = None
    flair_id: Optional[uuid.UUID] = None
    tag_ids: Optional[List[uuid.UUID]] = None


class ExperienceResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    takeaway: Optional[str] = None
    category: Optional[str] = "Personal"
    flair_id: Optional[uuid.UUID] = None
    flair: Optional[FlairResponse] = None
    tags: List[TagResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExperienceListResponse(BaseModel):
    items: List[ExperienceResponse]
    total: int
