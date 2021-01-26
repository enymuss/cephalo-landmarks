from raven import Client
from time import sleep
from typing import Tuple
import sys

from app.core.celery_app import celery_app

from app.core.config import settings

from fastapi import Depends
from app import crud, models
from sqlalchemy.orm import Session
from app.schemas.cephalo_landmark import LandmarkCreate
from app.db.session import SessionLocal

from app.nn_models.cephalo import cephalo_predict

client_sentry = Client(settings.SENTRY_DSN)

def predict_landmark_for_image(image_path: str, landmark_number: int) -> Tuple[float, float]:
    print(f"Start worker with {image_path} and {landmark_number}")
    return cephalo_predict.get_prediction(img_path=image_path, landmark=landmark_number)

@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"

@celery_app.task(acks_late=True)
def cephalo_celery(cephalo_id: int, file_path: str, landmark: int) -> str:
    predict_x, predict_y = predict_landmark_for_image(image_path=file_path, landmark_number=landmark)
    print(f" Returned {predict_x}, {predict_y}")
    landmark: LandmarkCreate = LandmarkCreate(landmark_number=landmark, landmark_x=predict_x, landmark_y=predict_y)
    landmark_db = crud.landmark.create_with_cephalo(
        db=SessionLocal(),
        obj_in=landmark,
        cephalo_id=cephalo_id
    )
    return f"cephalo_id: {cephalo_id}, file_path: {file_path}, landmark: {landmark}, landamrk_id: {landmark_db.id}"
