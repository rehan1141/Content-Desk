from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.idea_service import IdeaService
from app.schemas.idea import QuickCaptureCreate, IdeaResponse
from app.models.enums import IdeaStatus

router = APIRouter(prefix="/inbox", tags=["Inbox"])


@router.post(
    "/quick-capture",
    response_model=IdeaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Frictionless Quick Capture",
    description="Save a raw thought immediately with zero mandatory title, tags, or platform metadata."
)
def quick_capture(
    payload: QuickCaptureCreate,
    db: Session = Depends(get_db)
):
    service = IdeaService(db)
    return service.quick_capture(payload)


@router.get(
    "",
    response_model=List[IdeaResponse],
    summary="List Inbox Thoughts",
    description="Fetch all raw thoughts currently sitting in the Inbox."
)
def list_inbox_thoughts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = IdeaService(db)
    items, _ = service.list_ideas(status=IdeaStatus.RAW, skip=skip, limit=limit)
    return items
