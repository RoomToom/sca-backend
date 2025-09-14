from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class TargetIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=1, max_length=100)
    notes: Optional[str] = None

class MissionCreate(BaseModel):
    targets: List[TargetIn]
    assigned_cat_id: Optional[int] = None

class TargetOut(BaseModel):
    id: int
    name: str
    country: str
    notes: str | None
    is_complete: bool
    model_config = ConfigDict(from_attributes=True)

class MissionOut(BaseModel):
    id: int
    assigned_cat_id: int | None
    is_complete: bool
    targets: list[TargetOut]
    model_config = ConfigDict(from_attributes=True)
