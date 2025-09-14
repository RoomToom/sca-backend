from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...core.config import settings
from ...core.db import Base, engine
from ...core.catapi import validate_breed
from ...models.cat import Cat
from ...models.mission import Mission
from ...schemas.cats import CatCreate, CatOut, CatUpdateSalary
from ..deps import get_db_dep

Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/cats", tags=["cats"])

@router.post("", response_model=CatOut, status_code=201)
async def create_cat(payload: CatCreate, db: Session = Depends(get_db_dep)):
    if not await validate_breed(payload.breed, settings.CAT_API_URL, settings.CAT_API_KEY):
        raise HTTPException(status_code=422, detail="Invalid breed")
    cat = Cat(
        name=payload.name,
        years_experience=payload.years_experience,
        breed=payload.breed,
        salary=payload.salary,
    )
    db.add(cat); db.commit(); db.refresh(cat)
    return cat

@router.get("", response_model=list[CatOut])
def list_cats(db: Session = Depends(get_db_dep)):
    return db.query(Cat).all()

@router.get("/{cat_id}", response_model=CatOut)
def get_cat(cat_id: int, db: Session = Depends(get_db_dep)):
    cat = db.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat

@router.patch("/{cat_id}", response_model=CatOut)
def update_salary(cat_id: int, payload: CatUpdateSalary, db: Session = Depends(get_db_dep)):
    cat = db.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    cat.salary = float(payload.salary)
    db.add(cat); db.commit(); db.refresh(cat)
    return cat

@router.delete("/{cat_id}", status_code=204)
def delete_cat(cat_id: int, db: Session = Depends(get_db_dep)):
    cat = db.get(Cat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    db.delete(cat); db.commit()
    return
