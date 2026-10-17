from fastapi import APIRouter, Depends
from app.core.config import Settings, get_settings
from app.services.gemini_service import GeminiService

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check(settings: Settings = Depends(get_settings)):
    gemini = GeminiService()
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "gemini": {
            "model": settings.gemini_model,
            "is_configured": gemini.is_configured,
            "mode": "live_gemini" if gemini.is_configured else "pediatric_engine_fallback",
        },
    }
