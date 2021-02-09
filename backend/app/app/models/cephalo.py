from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .cephalo_landmark import Cephalo_Landmark # noqa: F401
    from .cephalo_measurement import Cephalo_Measurement

class Cephalo(Base):
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, index=True)
    px_per_cm = Column(Integer)
    landmarks = relationship("Cephalo_Landmark", back_populates="cephalo")
    measurements = relationship("Cephalo_Measurement", back_populates="cephalo")
