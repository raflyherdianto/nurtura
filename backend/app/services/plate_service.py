from typing import List, Optional
from app.schemas.child import ChildContext
from app.schemas.plate import PlateAuditResponse
from app.services.gemini_service import GeminiService


class PlateService:
    def __init__(self, gemini_service: GeminiService):
        self.gemini = gemini_service

    async def audit_plate_upload(
        self,
        child: ChildContext,
        meal_time: str,
        image_bytes: Optional[bytes] = None,
        image_mime: Optional[str] = None,
        selected_items: Optional[List[str]] = None,
        notes: Optional[str] = None,
    ) -> PlateAuditResponse:
        return await self.gemini.audit_plate(
            child=child,
            meal_time=meal_time,
            image_bytes=image_bytes,
            image_mime=image_mime,
            selected_items=selected_items,
            notes=notes,
        )
