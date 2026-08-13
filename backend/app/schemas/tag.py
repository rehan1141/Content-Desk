import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str
    color: Optional[str] = "#6366f1"


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
