from fastapi import APIRouter
from app.api.v1.endpoints import health, milestone, plate, rag

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(milestone.router)
api_router.include_router(plate.router)
api_router.include_router(rag.router, prefix="/rag", tags=["Clinical RAG"])

