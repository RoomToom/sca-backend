from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..core.db import Base

class Cat(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    years_experience = Column(Integer, nullable=False, default=0)
    breed = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False, default=0.0)
    current_mission_id = Column(Integer, ForeignKey("missions.id"), nullable=True)
