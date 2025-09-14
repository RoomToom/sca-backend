from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...core.db import Base, engine
from ...models.mission import Mission
from ...models.target import Target
from ...models.cat import Cat
from ...schemas.missions import MissionCreate, MissionOut
from ..deps import get_db_dep

Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/missions", tags=["missions"])

@router.post("", response_model=MissionOut, status_code=201)
def create_mission(payload: MissionCreate, db: Session = Depends(get_db_dep)):
    # 1–3 targets
    if not (1 <= len(payload.targets) <= 3):
        raise HTTPException(status_code=422, detail="Mission must have 1-3 targets")

    # Pre-check assigned cat (if any)
    cat: Cat | None = None
    if payload.assigned_cat_id is not None:
        cat = db.get(Cat, payload.assigned_cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        if cat.current_mission_id is not None:
            raise HTTPException(status_code=400, detail="Cat already assigned to a mission")

    # Create mission
    mission = Mission(is_complete=False)
    db.add(mission)
    db.commit()
    db.refresh(mission)

    # Create targets
    for t in payload.targets:
        target = Target(
            mission_id=mission.id,
            name=t.name,
            country=t.country,
            notes=t.notes or "",
            is_complete=False,
        )
        db.add(target)
    db.commit()
    db.refresh(mission)

    # Assign cat if provided
    if cat is not None:
        mission.assigned_cat_id = cat.id
        cat.current_mission_id = mission.id
        db.add(mission)
        db.add(cat)
        db.commit()
        db.refresh(mission)

    return mission

@router.get("", response_model=list[MissionOut])
def list_missions(db: Session = Depends(get_db_dep)):
    return db.query(Mission).all()

@router.get("/{mission_id}", response_model=MissionOut)
def get_mission(mission_id: int, db: Session = Depends(get_db_dep)):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.delete("/{mission_id}", status_code=204)
def delete_mission(mission_id: int, db: Session = Depends(get_db_dep)):
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission.assigned_cat_id is not None:
        raise HTTPException(status_code=400, detail="Cannot delete an assigned mission")
    db.delete(mission)
    db.commit()
    return

@router.patch("/{mission_id}/assign", response_model=MissionOut)
def assign_mission(mission_id: int, cat_id: int, db: Session = Depends(get_db_dep)):
    # Load entities
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    cat = db.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    # Guards
    if mission.is_complete:
        raise HTTPException(status_code=400, detail="Cannot assign a completed mission")
    if mission.assigned_cat_id is not None:
        raise HTTPException(status_code=400, detail="Mission already assigned")
    if cat.current_mission_id is not None:
        raise HTTPException(status_code=400, detail="Cat already assigned to a mission")

    # Assign
    mission.assigned_cat_id = cat.id
    cat.current_mission_id = mission.id
    db.add(mission)
    db.add(cat)
    db.commit()
    db.refresh(mission)
    return mission
