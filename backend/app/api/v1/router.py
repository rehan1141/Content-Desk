from fastapi import APIRouter
from app.api.v1.endpoints import inbox, ideas, experiences

api_router = APIRouter()

api_router.include_router(inbox.router)
api_router.include_router(ideas.router)
api_router.include_router(experiences.router)
