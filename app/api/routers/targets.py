from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...models.target import Target
from ...models.mission import Mission
from ...schemas.targets import TargetNotesUpdate
from ...services.missions import freeze_guard, maybe_complete_mission
from ..deps import get_db_dep

router = APIRouter(prefix="/targets", tags=["targets"])

@router.patch("/{target_id}/notes")
def update_notes(target_id: int, payload: TargetNotesUpdate, db: Session = Depends(get_db_dep)):
    target = db.get(Target, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    mission = db.get(Mission, target.mission_id)
    freeze_guard(target, mission)
    target.notes = payload.notes
    db.add(target)
    db.commit()
    return {"status": "ok"}

@router.patch("/{target_id}/complete")
def complete_target(target_id: int, db: Session = Depends(get_db_dep)):
    target = db.get(Target, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    mission = db.get(Mission, target.mission_id)
    target.is_complete = True
    db.add(target)
    db.commit()

    # доводимо місію до completed, якщо всі таргети зачинені (логіка всередині сервісу)
    maybe_complete_mission(db, mission)
    return {"status": "ok"}
