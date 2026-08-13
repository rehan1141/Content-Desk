from fastapi import APIRouter
from app.api.v1.endpoints import inbox, ideas

api_router = APIRouter()

api_router.include_router(inbox.router)
api_router.include_router(ideas.router)
