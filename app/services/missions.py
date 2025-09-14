from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.mission import Mission
from ..models.target import Target

def freeze_guard(target: Target, mission: Mission):
    if target.is_complete or mission.is_complete:
        raise HTTPException(status_code=400, detail="Notes are frozen")

def maybe_complete_mission(db: Session, mission: Mission):
    if all(t.is_complete for t in mission.targets):
        mission.is_complete = True
        db.add(mission)
        db.commit()
        db.refresh(mission)
