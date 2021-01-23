from raven import Client
from time import sleep
from typing import Tuple

from app.core.celery_app import celery_app

from app.core.config import settings

from fastapi import Depends
from app import crud, models
from sqlalchemy.orm import Session
from app.schemas.cephalo_landmark import LandmarkCreate
from app.db.session import SessionLocal

client_sentry = Client(settings.SENTRY_DSN)

def predict_landmark_for_image(image_path: str, landmark_number: int) -> Tuple[float, float]:
    return (250.0, 250.0)

@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"

@celery_app.task(acks_late=True)
def cephalo_celery(cephalo_id: int, file_path: str, landmark: int) -> str:
    predict_x, predict_y = predict_landmark_for_image(image_path=file_path, landmark_number=landmark)
    landmark: LandmarkCreate = LandmarkCreate(landmark_number=landmark, landmark_x=predict_x, landmark_y=predict_y)
    landmark_db = crud.landmark.create_with_cephalo(
        db=SessionLocal(),
        obj_in=landmark,
        cephalo_id=cephalo_id
    )
    return f"cephalo_id: {cephalo_id}, file_path: {file_path}, landmark: {landmark}, landamrk_id: {landmark_db.id}"
