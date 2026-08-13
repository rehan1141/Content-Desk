import uuid
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.experience_service import ExperienceService
from app.schemas.experience import ExperienceCreate, ExperienceUpdate, ExperienceResponse, ExperienceListResponse

router = APIRouter(prefix="/experiences", tags=["Experiences"])


@router.post(
    "",
    response_model=ExperienceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Experience",
    description="Store a personal story, project milestone, mistake, or lesson in the vault."
)
def create_experience(
    payload: ExperienceCreate,
    db: Session = Depends(get_db)
):
    service = ExperienceService(db)
    return service.create_experience(payload)


@router.get(
    "",
    response_model=ExperienceListResponse,
    summary="List Experiences",
    description="Retrieve personal experiences with optional category filtering."
)
def list_experiences(
    category: Optional[str] = Query(None, description="Filter by category (e.g. Personal, Career, Technical, Mistakes)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    service = ExperienceService(db)
    items, total = service.list_experiences(category=category, skip=skip, limit=limit)
    return ExperienceListResponse(items=items, total=total)


@router.get(
    "/{exp_id}",
    response_model=ExperienceResponse,
    summary="Get Experience Details",
    description="Fetch a single experience by UUID primary key."
)
def get_experience(
    exp_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    service = ExperienceService(db)
    return service.get_experience(exp_id)


@router.patch(
    "/{exp_id}",
    response_model=ExperienceResponse,
    summary="Update Experience",
    description="Update title, description, takeaway, category, flair, or tags."
)
def update_experience(
    exp_id: uuid.UUID,
    payload: ExperienceUpdate,
    db: Session = Depends(get_db)
):
    service = ExperienceService(db)
    return service.update_experience(exp_id, payload)


@router.delete(
    "/{exp_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Experience",
    description="Permanently delete an experience from the vault."
)
def delete_experience(
    exp_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    service = ExperienceService(db)
    service.delete_experience(exp_id)
