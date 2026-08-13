import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.idea_service import IdeaService
from app.schemas.idea import IdeaCreate, IdeaUpdate, IdeaResponse, IdeaListResponse
from app.models.enums import IdeaStatus

router = APIRouter(prefix="/ideas", tags=["Ideas"])


@router.post(
    "",
    response_model=IdeaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Idea",
    description="Create a structured Idea with optional title, prompts, flair, and tags."
)
def create_idea(
    payload: IdeaCreate,
    db: Session = Depends(get_db)
):
    service = IdeaService(db)
    return service.create_idea(payload)


@router.get(
    "",
    response_model=IdeaListResponse,
    summary="List Ideas",
    description="Retrieve ideas with optional status filter and pagination."
)
def list_ideas(
    status: Optional[IdeaStatus] = Query(None, description="Filter by status (RAW, DEVELOPING, DRAFT, READY, ARCHIVED)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    service = IdeaService(db)
    items, total = service.list_ideas(status=status, skip=skip, limit=limit)
    return IdeaListResponse(items=items, total=total)


@router.get(
    "/{idea_id}",
    response_model=IdeaResponse,
    summary="Get Idea Details",
    description="Fetch a single idea by UUID primary key."
)
def get_idea(
    idea_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    service = IdeaService(db)
    return service.get_idea(idea_id)


@router.patch(
    "/{idea_id}",
    response_model=IdeaResponse,
    summary="Update Idea",
    description="Update fields, status, or thinking prompts for an existing idea."
)
def update_idea(
    idea_id: uuid.UUID,
    payload: IdeaUpdate,
    db: Session = Depends(get_db)
):
    service = IdeaService(db)
    return service.update_idea(idea_id, payload)


@router.delete(
    "/{idea_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Idea",
    description="Permanently delete an idea from database."
)
def delete_idea(
    idea_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    service = IdeaService(db)
    service.delete_idea(idea_id)
