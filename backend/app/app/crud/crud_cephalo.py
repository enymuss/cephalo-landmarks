from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cephalo import Cephalo
from app.schemas.cephalo import CephaloCreate, CephaloUpdate

class CRUDCephalo(CRUDBase[Cephalo, CephaloCreate, CephaloUpdate]):
    def create(self, db: Session, *, obj_in: CephaloCreate, file_path: str) -> Cephalo:
        db_obj = Cephalo(
            file_path=file_path,
            px_per_cm=obj_in.px_per_cm,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # load the model and do calculations

        return db_obj

    def update(
        self, db:Session, *, db_obj: Cephalo, obj_in: Union[CephaloUpdate, Dict[str, Any]]
    ) -> Cephalo:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

cephalo = CRUDCephalo(Cephalo)
