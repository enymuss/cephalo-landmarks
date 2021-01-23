from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.celery_app import celery_app

import shutil
import os
from pathlib import Path

UPLOAD_FOLDER = "./uploads/cephalo/"
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

router = APIRouter()

@router.get("/landmarks", response_model=List[schemas.Landmark])
def read_landmarks_for_cephalo(
    *,
    db: Session = Depends(deps.get_db),
    cephalo_id: int,
) -> Any:
    """
    Retrive all landmarks for given cephalometric image by id.
    """
    landmarks = crud.landmark.get_landmarks_by_cephalo(db=db, cephalo_id=cephalo_id)
    return landmarks

@router.post("/predict", response_model=schemas.Cephalo, status_code=201)
async def create_prediction(
    *,
    db: Session = Depends(deps.get_db),
    cephalo_in: schemas.CephaloCreate = Depends(schemas.CephaloCreate.as_form),
    file: UploadFile = File(...),
) -> Any:
    """
    Create new cephalo prediction.
    """
    saved_file_path = os.path.join(UPLOAD_FOLDER, "destination.png")
    with open(saved_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    cephalo = crud.cephalo.create(db=db, obj_in=cephalo_in, file_path=saved_file_path)
    # print({"cephalo filename": file.filename})
    for i in range(1):
        celery_app.send_task("app.worker.cephalo_celery", args=[cephalo.id, saved_file_path, i])
    return cephalo
