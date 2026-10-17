from typing import Any, List, Literal, Optional, Union
from pydantic import BaseModel, Field, field_validator
from app.schemas.child import ChildContext
from app.schemas.common import LocalizedString

FoodKind = Literal["animal", "fat", "carb", "veg", "plant"]
MacroRating = Literal["low", "ok", "good"]
TextureStatus = Literal["fine", "ok", "coarse"]
MealTimeType = Literal["pagi", "siang", "malam", "camilan"]


class FoodDetectedItem(BaseModel):
    name: LocalizedString = Field(..., description="Name of the food identified")
    kind: FoodKind = Field(default="carb", description="Nutritional category")
    confidence: Optional[float] = Field(default=None, description="Detection confidence score")

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, v: Any) -> Any:
        if isinstance(v, str):
            return LocalizedString(id=v, en=v)
        if isinstance(v, dict):
            id_val = v.get("id") or v.get("en") or "Makanan"
            en_val = v.get("en") or v.get("id") or "Food"
            return LocalizedString(id=id_val, en=en_val)
        return v

    @field_validator("kind", mode="before")
    @classmethod
    def normalize_kind(cls, v: Any) -> Any:
        if isinstance(v, str):
            v_lower = v.lower()
            if any(k in v_lower for k in ["anim", "hewani", "meat", "daging", "ayam", "ikan", "telur", "hati"]):
                return "animal"
            if any(k in v_lower for k in ["fat", "lemak", "oil", "minyak", "santan", "butter", "mentega"]):
                return "fat"
            if any(k in v_lower for k in ["veg", "sayur", "serat", "vegetable"]):
                return "veg"
            if any(k in v_lower for k in ["plant", "nabati", "tempe", "tahu", "kacang"]):
                return "plant"
            if any(k in v_lower for k in ["carb", "karbo", "nasi", "rice", "bubur", "kentang"]):
                return "carb"
        return v if v in ["animal", "fat", "carb", "veg", "plant"] else "carb"


class TextureVerdictSchema(BaseModel):
    status: TextureStatus = Field(..., description="'fine' (too fine), 'ok' (age-appropriate), 'coarse' (too hard/choking risk)")
    title: LocalizedString = Field(..., description="Texture verdict title")
    description: LocalizedString = Field(..., description="Actionable oral-motor feedback based on child's age")


class MacroInfoSchema(BaseModel):
    key: Literal["animal", "fat", "carb"] = Field(..., description="Macro key")
    name: LocalizedString = Field(..., description="Display name of macro")
    rating: MacroRating = Field(..., description="Evaluation rating: low, ok, good")
    percentage: int = Field(..., ge=0, le=100, description="Visual gauge percentage")
    label: LocalizedString = Field(..., description="Rating label (e.g., Kurang / Cukup / Baik)")
    hint: Optional[LocalizedString] = Field(default=None, description="Specific guidance or caveat")
    recipe: Optional[LocalizedString] = Field(default=None, description="Quick upgrade recommendation")


class BoosterRecipeSchema(BaseModel):
    name: LocalizedString = Field(..., description="Quick recipe name (e.g. Telur Orak-Arik Mentega)")
    prep_time: LocalizedString = Field(..., description="Preparation time (e.g. 5 Menit)")
    ingredients: List[LocalizedString] = Field(..., description="Affordable, accessible ingredients")
    instructions: List[LocalizedString] = Field(..., description="Simple, step-by-step instructions")


class UpgradePlanSchema(BaseModel):
    summary: LocalizedString = Field(..., description="Next-meal nutritional repair summary")
    suggestions: List[LocalizedString] = Field(..., description="Immediate tips for the parent")
    booster_recipe: Optional[BoosterRecipeSchema] = Field(default=None, description="5-minute budget-friendly booster recipe")


class PlateAuditJsonRequest(BaseModel):
    child: ChildContext
    meal_time: MealTimeType = Field(default="siang", description="Meal time slot")
    selected_items: Optional[List[str]] = Field(default=None, description="Food items selected manually")
    notes: Optional[str] = Field(default=None, description="Additional plate notes or ingredients")


class PlateAuditResponse(BaseModel):
    id: str = Field(..., description="Unique plate audit ID")
    meal_time: MealTimeType = Field(..., description="Evaluated meal slot")
    detected_foods: List[FoodDetectedItem] = Field(..., description="Identified food components")
    detected_texture: str = Field(..., description="Physical texture identified")
    texture_verdict: TextureVerdictSchema = Field(..., description="Oral-motor age appropriateness")
    macros: List[MacroInfoSchema] = Field(..., description="Three key pillars: animal protein, fat, carb")
    deficient_macros: List[str] = Field(..., description="List of deficient macro keys needing immediate upgrade")
    upgrade_plan: UpgradePlanSchema = Field(..., description="Next-meal action plan and quick booster recipe")
    disclaimer: LocalizedString = Field(..., description="Pediatric disclaimer notice")
    rag_sources: Optional[List[str]] = Field(default_factory=list, description="Grounding clinical RAG sources")
