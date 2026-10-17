from typing import Optional, Literal
from pydantic import BaseModel, Field


class ChildContext(BaseModel):
    name: str = Field(default="Anak", min_length=1, max_length=50, description="Child's display name")
    gender: Optional[Literal["boy", "girl"]] = Field(default="boy", description="Child's gender ('boy' | 'girl')")
    age_months: int = Field(..., ge=0, le=60, description="Child's age in months (0-60)")
    weight_kg: float = Field(..., gt=0.0, le=50.0, description="Child's weight in kilograms")
    height_cm: float = Field(..., gt=0.0, le=150.0, description="Child's height in centimeters")
