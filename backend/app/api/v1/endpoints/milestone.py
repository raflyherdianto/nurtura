import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.milestone import MilestoneEvaluationRequest, MilestoneEvaluationResponse
from app.services.gemini_service import GeminiService
from app.services.milestone_service import MilestoneService

router = APIRouter(prefix="/milestone", tags=["Milestone & Playbook"])
logger = logging.getLogger(__name__)


def get_milestone_service() -> MilestoneService:
    return MilestoneService(gemini_service=GeminiService())


@router.post(
    "/evaluate",
    response_model=MilestoneEvaluationResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate child milestone observation and craft 3-day playbook",
)
async def evaluate_milestone(
    payload: MilestoneEvaluationRequest,
    service: MilestoneService = Depends(get_milestone_service),
) -> MilestoneEvaluationResponse:
    """
    Submits parent's natural language observation along with child's age/anthropometrics.
    Returns WHO/CDC developmental benchmark and a personalized 3-Day Home Stimulation Playbook.
    """
    try:
        return await service.evaluate_observation(payload)
    except Exception as exc:
        logger.error("Live Gemini milestone evaluation failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Live Gemini evaluation is unavailable. No sample result was generated.",
        ) from exc
