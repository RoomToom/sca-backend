from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..core.db import Base

class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    assigned_cat_id = Column(Integer, ForeignKey("cats.id"), nullable=True)
    is_complete = Column(Boolean, default=False, nullable=False)

    targets = relationship("Target", back_populates="mission", cascade="all, delete-orphan")
