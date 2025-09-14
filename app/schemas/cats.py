from pydantic import BaseModel, Field, conint, confloat, ConfigDict

class CatCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    years_experience: conint(ge=0, le=50)
    breed: str = Field(min_length=1, max_length=100)
    salary: confloat(ge=0)

class CatOut(BaseModel):
    id: int
    name: str
    years_experience: int
    breed: str
    salary: float
    current_mission_id: int | None
    model_config = ConfigDict(from_attributes=True)

class CatUpdateSalary(BaseModel):
    salary: confloat(ge=0)
