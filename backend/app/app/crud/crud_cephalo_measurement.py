from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cephalo_measurement import Cephalo_Measurement
from app.models.cephalo import Cephalo
from app.schemas.cephalo_measurement import MeasurementCreate, MeasurementUpdate

from app.nn_models.cephalo import cephaloConstants
from app.crud.crud_cephalo_landmark import landmark
from app.crud.crud_cephalo import cephalo

class CRUDMeasurement(CRUDBase[Cephalo_Measurement, MeasurementCreate, MeasurementUpdate]):
    def create_with_cephalo(
        self, db:Session, *, cephalo_id: int
    ) -> List[Cephalo_Measurement]:
        new_measurements = []
        landmarks_dict = {}

        # get all landmarks for cephalo_id
        landmarks = landmark.get_landmarks_by_cephalo(db=db, cephalo_id=cephalo_id)

        if landmarks is None or len(landmarks) < 3:
            return None

        for instance in landmarks:
            landmarks_dict[instance.landmark_number] = [instance.landmark_x, instance.landmark_y]

        for measurement_points in cephaloConstants.angles_list:
            if cephaloConstants.can_calculate_measurement(measurement_points):
                landmark_ids = []
                measurement_value = 0
                for x in measurement_points:
                    landmark_ids.extend(cephaloConstants.acronym_to_landmark_ids(x))
                print(landmark_ids)
                if len(landmark_ids) == 3:
                    measurement_value = cephaloConstants.angle_between_three_points(landmarks_dict[landmark_ids[0]], landmarks_dict[landmark_ids[1]], landmarks_dict[landmark_ids[2]])
                else:
                    measurement_value = cephaloConstants.angle_between_four_points(landmarks_dict[landmark_ids[0]], landmarks_dict[landmark_ids[1]], landmarks_dict[landmark_ids[2]], landmarks_dict[landmark_ids[3]])

                measurement_value = round(measurement_value, 1)
                new_measurement = MeasurementCreate(measurement_name="-".join(measurement_points), unit="deg", value=measurement_value)
                new_measurements.append(new_measurement)

        px_per_cm = cephalo.get(db, cephalo_id).px_per_cm
        print(px_per_cm)
        for measurement_points in cephaloConstants.distance_list:
            if cephaloConstants.can_calculate_measurement(measurement_points):
                landmark_ids = []
                measurement_value = 0
                for x in measurement_points:
                    landmark_ids.extend(cephaloConstants.acronym_to_landmark_ids(x))

                if len(landmark_ids) == 3:
                    measurement_value = cephaloConstants.calculate_distance(px_per_cm, landmarks_dict[landmark_ids[0]], landmarks_dict[landmark_ids[1]], landmarks_dict[landmark_ids[2]])
                else:
                    measurement_value = cephaloConstants.calculate_distance(px_per_cm, landmarks_dict[landmark_ids[0]], landmarks_dict[landmark_ids[1]], landmarks_dict[landmark_ids[2]], landmarks_dict[landmark_ids[3]])

                measurement_value = round(measurement_value, 3)
                new_measurement = MeasurementCreate(measurement_name="-".join(measurement_points), unit="cm", value=measurement_value)
                new_measurements.append(new_measurement)


        db_objs = []
        for n_measurement in new_measurements:
            obj_in_data = jsonable_encoder(n_measurement)
            db_obj = self.model(**obj_in_data, cephalo_id=cephalo_id)
            db_objs.append(db_obj)

        db.add_all(db_objs)
        db.commit()
        for db_obj in db_objs:
            db.refresh(db_obj)
        return db_objs

    def get_measurements_by_cephalo(
        self, db: Session, *, cephalo_id: int
    ) -> List[Cephalo_Measurement]:
        return (
            db.query(self.model)
            .filter(Cephalo_Measurement.cephalo_id == cephalo_id)
            .all()
        )

    def remove(
        self, db: Session, *,  cephalo_id: int
    ) -> List[Cephalo_Measurement]:
        obj_q = db.query(self.model).filter(Cephalo_Measurement.cephalo_id == cephalo_id)
        obj = obj_q.all()
        obj_q.delete()
        db.commit()
        return obj

measurement = CRUDMeasurement(Cephalo_Measurement)
