from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from app.schemas.child import ChildContext
from app.schemas.common import LocalizedString


class PlaybookDaySchema(BaseModel):
    day: int = Field(..., ge=1, le=3, description="Day number (1, 2, or 3)")
    item: LocalizedString = Field(..., description="Zero-cost household item used")
    title: LocalizedString = Field(..., description="Daily playful stimulation activity title")
    steps: List[LocalizedString] = Field(..., min_length=1, description="Sequential steps for the parent")


class MilestoneEvaluationRequest(BaseModel):
    child: ChildContext
    observation_note: str = Field(..., min_length=3, max_length=1000, description="Parent's natural language observation")
    checked_milestones: Optional[List[str]] = Field(default_factory=list, description="List of observed milestones already checked")


class MilestoneEvaluationResponse(BaseModel):
    id: str = Field(..., description="Unique evaluation session ID")
    status_type: Literal["ok", "watch", "alert"] = Field(..., description="Clinical triage status")
    status_title: LocalizedString = Field(..., description="Clear status title")
    status_desc: LocalizedString = Field(..., description="Empathetic clinical explanation")
    ref: LocalizedString = Field(..., description="WHO / CDC / Kemenkes milestone reference")
    safety: LocalizedString = Field(..., description="Pediatric safety alert or red flag advice")
    focus_area: LocalizedString = Field(..., description="Primary developmental focus area")
    playbook: List[PlaybookDaySchema] = Field(..., min_length=3, max_length=3, description="3-Day home stimulation curriculum")
    rag_sources: List[str] = Field(default_factory=list, description="Retrieved RAG knowledge base clinical guidelines")
