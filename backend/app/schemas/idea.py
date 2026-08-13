import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.models.enums import IdeaStatus
from app.schemas.tag import TagResponse
from app.schemas.flair import FlairResponse


class QuickCaptureCreate(BaseModel):
    """Frictionless quick capture payload: only raw_thought required."""
    raw_thought: str


class IdeaCreate(BaseModel):
    raw_thought: str
    title: Optional[str] = None
    development_notes: Optional[str] = None
    status: Optional[IdeaStatus] = IdeaStatus.RAW
    why_prompt: Optional[str] = None
    what_happened_prompt: Optional[str] = None
    actual_point_prompt: Optional[str] = None
    flair_id: Optional[uuid.UUID] = None
    experience_id: Optional[uuid.UUID] = None
    tag_ids: Optional[List[uuid.UUID]] = []


class IdeaUpdate(BaseModel):
    title: Optional[str] = None
    raw_thought: Optional[str] = None
    development_notes: Optional[str] = None
    status: Optional[IdeaStatus] = None
    why_prompt: Optional[str] = None
    what_happened_prompt: Optional[str] = None
    actual_point_prompt: Optional[str] = None
    flair_id: Optional[uuid.UUID] = None
    experience_id: Optional[uuid.UUID] = None
    tag_ids: Optional[List[uuid.UUID]] = None


class IdeaResponse(BaseModel):
    id: uuid.UUID
    title: Optional[str] = None
    raw_thought: str
    development_notes: Optional[str] = None
    status: IdeaStatus
    why_prompt: Optional[str] = None
    what_happened_prompt: Optional[str] = None
    actual_point_prompt: Optional[str] = None
    flair_id: Optional[uuid.UUID] = None
    experience_id: Optional[uuid.UUID] = None
    flair: Optional[FlairResponse] = None
    tags: List[TagResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IdeaListResponse(BaseModel):
    items: List[IdeaResponse]
    total: int
