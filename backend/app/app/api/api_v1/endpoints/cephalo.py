from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/predict", response_model=schemas.Cephalo)
async def create_prediction(
    *,
    db: Session = Depends(deps.get_db),
    file_path: str = Form(...),
    px_per_cm: int = Form(...),
    file: UploadFile = File(...),
) -> Any:
    """
    Create new cephalo prediction.
    """
    print("Helo")
    cephalo_in = {
        'file_path': "asd",
        'px_per_cm': 2
    }
    cephalo_in = schemas.CephaloCreate(**cephalo_in)
    # item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    cephalo = crud.cephalo.create(db=db, obj_in=cephalo_in)
    # print({"cephalo filename": file.filename})
    return cephalo
