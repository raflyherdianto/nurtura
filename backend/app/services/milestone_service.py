from app.schemas.child import ChildContext
from app.schemas.milestone import MilestoneEvaluationRequest, MilestoneEvaluationResponse
from app.services.gemini_service import GeminiService


class MilestoneService:
    def __init__(self, gemini_service: GeminiService):
        self.gemini = gemini_service

    async def evaluate_observation(
        self,
        request: MilestoneEvaluationRequest,
    ) -> MilestoneEvaluationResponse:
        return await self.gemini.evaluate_milestones(
            child=request.child,
            observation=request.observation_note,
            checked_milestones=request.checked_milestones,
        )
