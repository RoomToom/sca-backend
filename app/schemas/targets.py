from pydantic import BaseModel, Field

class TargetNotesUpdate(BaseModel):
    notes: str = Field(min_length=0, max_length=2000)
