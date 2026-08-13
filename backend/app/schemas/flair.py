import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict


class FlairBase(BaseModel):
    name: str
    color: Optional[str] = "#8b5cf6"
    description: Optional[str] = None


class FlairCreate(FlairBase):
    pass


class FlairResponse(FlairBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)
