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

@router.get("/cephalo/{id}", response_model=schemas.Cephalo)
def read_cephalo(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    "Get cephalo data from db"
    return crud.cephalo.get(db, id)



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

@router.get("/measurements", response_model=List[schemas.Measurement])
def read_cephalo_measurements(
    *,
    db: Session = Depends(deps.get_db),
    cephalo_id: int,
) -> Any:
    """
    Retrive all measurements for given cephalometric image by id.
    """

    measurements = crud.measurement.get_measurements_by_cephalo(db=db, cephalo_id=cephalo_id)
    if (len(measurements) == 0):
        result = crud.measurement.create_with_cephalo(db=db, cephalo_id=cephalo_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Landmarks not found")
        measurements = crud.measurement.get_measurements_by_cephalo(db=db, cephalo_id=cephalo_id)

    return measurements

@router.put("/measurements", response_model=List[schemas.Measurement])
def put_cephalo_measurements(
    *,
    db: Session = Depends(deps.get_db),
    cephalo_id: int,
) -> Any:
    """
    Recalculate all measurements for given cephalometric image by id.
    """
    crud.measurement.remove(db=db, cephalo_id=cephalo_id)
    result = crud.measurement.create_with_cephalo(db=db, cephalo_id=cephalo_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Landmarks not found")
    measurements = crud.measurement.get_measurements_by_cephalo(db=db, cephalo_id=cephalo_id)

    return measurements

@router.delete("/measurements/{cephalo_id}", response_model=List[schemas.Measurement])
def delete_cephalo_measurements(
    *,
    db:Session = Depends(deps.get_db),
    cephalo_id: int
) -> Any:
    "Delete All measurements for given cephalo_id"
    measurements = crud.measurement.get_measurements_by_cephalo(db=db, cephalo_id=cephalo_id)
    if not measurements:
        raise HTTPException(status_code=404, detail="Measurements not found")

    item = crud.measurement.remove(db=db, cephalo_id=cephalo_id)
    return item

@router.post("/measurements", response_model=schemas.Measurement)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    cephalo_id: int,
) -> Any:
    """
    Create new measurement.
    """
    measurement = crud.measurement.create_with_cephalo(db=db, cephalo_id=cephalo_id)
    return measurement

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
    saved_file_path = os.path.join(UPLOAD_FOLDER, "destination.jpg")
    with open(saved_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    cephalo = crud.cephalo.create(db=db, obj_in=cephalo_in, file_path=saved_file_path)
    # print({"cephalo filename": file.filename})
    for i in range(0, 20):
        celery_app.send_task("app.worker.cephalo_celery", args=[cephalo.id, saved_file_path, i])
    return cephalo
