from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/predict", response_model=schemas.Item)
async def create_prediction(
    *,
    db: Session = Depends(deps.get_db),
    cephalo_in: schemas.CephaloCreate,
    file: UploadFile = File(...),
) -> Any:
    """
    Create new cephalo prediction
    """
    # item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    cephalo = crud.cephalo.create(db=db, obj_in=cephalo_in)
    print({"cephalo filename": file.filename})
    return cephalo
