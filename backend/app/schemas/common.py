from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class LocalizedString(BaseModel):
    id: str = Field(..., description="Indonesian text")
    en: str = Field(..., description="English text")


class StandardResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    message: Optional[str] = None
