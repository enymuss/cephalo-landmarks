from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cephalo_measurement import Cephalo_Measurement
from app.schemas.cephalo_measurement import MeasurementCreate, MeasurementUpdate

class CRUDMeasurement(CRUDBase[Cephalo_Measurement, MeasurementCreate, MeasurementUpdate]):
    def create_with_cephalo(
        self, db:Session, *, obj_in: MeasurementCreate, cephalo_id: int
    ) -> Cephalo_Measurement:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, cephalo_id=cephalo_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_measurements_by_cephalo(
        self, db: Session, *, cephalo_id: int
    ) -> List[Cephalo_Measurement]:
        return (
            db.query(self.model)
            .filter(Cephalo_Measurement.cephalo_id == cephalo_id)
            .all()
        )

measurement = CRUDMeasurement(Cephalo_Measurement)
