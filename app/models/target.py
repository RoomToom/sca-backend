from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..core.db import Base

class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    notes = Column(String(2000), nullable=True)
    is_complete = Column(Boolean, default=False, nullable=False)

    mission = relationship("Mission", back_populates="targets")
