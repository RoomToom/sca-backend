from fastapi import Depends
from sqlalchemy.orm import Session
from ..core.db import get_db

def get_db_dep(db: Session = Depends(get_db)):
    return db
