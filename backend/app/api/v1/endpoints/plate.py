from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from app.schemas.child import ChildContext
from app.schemas.plate import (
    MealTimeType,
    PlateAuditJsonRequest,
    PlateAuditResponse,
)
from app.services.gemini_service import GeminiService
from app.services.plate_service import PlateService

router = APIRouter(prefix="/plate", tags=["Smart Plate Vision"])


def get_plate_service() -> PlateService:
    return PlateService(gemini_service=GeminiService())


@router.post(
    "/audit",
    response_model=PlateAuditResponse,
    status_code=status.HTTP_200_OK,
    summary="Audit plate via JSON payload",
)
async def audit_plate_json(
    payload: PlateAuditJsonRequest,
    service: PlateService = Depends(get_plate_service),
) -> PlateAuditResponse:
    """
    Audits a child's meal composition from selected ingredients and parent notes.
    Evaluates anti-stunting macro pillars and age-appropriate oral-motor textures.
    """
    return await service.audit_plate_upload(
        child=payload.child,
        meal_time=payload.meal_time,
        selected_items=payload.selected_items,
        notes=payload.notes,
    )


@router.post(
    "/audit-upload",
    response_model=PlateAuditResponse,
    status_code=status.HTTP_200_OK,
    summary="Audit plate via photo upload",
)
async def audit_plate_upload(
    image: UploadFile = File(..., description="Plate meal photo (JPEG, PNG, WEBP)"),
    child_name: str = Form(default="Anak"),
    age_months: int = Form(...),
    weight_kg: float = Form(...),
    height_cm: float = Form(...),
    meal_time: MealTimeType = Form(default="siang"),
    notes: Optional[str] = Form(default=None),
    service: PlateService = Depends(get_plate_service),
) -> PlateAuditResponse:
    """
    Multimodal audit: Ingests a photo of the child's plate, analyzes oral-motor texture,
    detects animal protein and healthy fats, and generates a 5-minute booster recipe.
    """
    image_bytes = await image.read()
    image_mime = image.content_type or "image/jpeg"

    child = ChildContext(
        name=child_name,
        age_months=age_months,
        weight_kg=weight_kg,
        height_cm=height_cm,
    )

    return await service.audit_plate_upload(
        child=child,
        meal_time=meal_time,
        image_bytes=image_bytes,
        image_mime=image_mime,
        notes=notes,
    )
