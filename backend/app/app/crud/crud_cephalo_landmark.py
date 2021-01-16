from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cephalo_landmark import Cephalo_Landmark
from app.schemas.cephalo_landmark import LandmarkCreate, LandmarkUpdate

class CRUDLandmark(CRUDBase[Cephalo_Landmark, LandmarkCreate, LandmarkUpdate]):
    def create_with_cephalo(
        self, db:Session, *, obj_in: LandmarkCreate, cephalo_id: int
    ) -> Cephalo_Landmark:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, cephalo_id=cephalo_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_landmarks_by_cephalo(
        self, db: Session, *, cephalo_id: int
    ) -> List[Cephalo_Landmark]:
        return (
            db.query(self.model)
            .filter(Cephalo_Landmark.cephalo_id == cephalo_id)
            .all()
        )

landmark = CRUDLandmark(Cephalo_Landmark)
