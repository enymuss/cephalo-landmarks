from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .cephalo import Cephalo # noqa: F401

class Cephalo_Landmark(Base):
    id = Column(Integer, primary_key=True, index=True)
    landmark_number = Column(Integer, index=True)
    landmark_x = Column(Float)
    landmark_y = Column(Float)
    cephalo_id = Column(Integer, ForeignKey("cephalo.id"))
    cephalo = relationship("Cephalo", back_populates="landmarks")
