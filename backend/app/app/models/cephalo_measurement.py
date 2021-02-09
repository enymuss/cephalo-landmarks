from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .cephalo import Cephalo # noqa: F401

class Cephalo_Measurement(Base):
    id = Column(Integer, primary_key=True, index=True)
    measurement_name = Column(String)
    unit = Column(String)
    value = Column(Float)
    cephalo_id = Column(Integer, ForeignKey("cephalo.id"))
    cephalo = relationship("Cephalo", back_populates="measurements")
