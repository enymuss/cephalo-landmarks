from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cephalo_measurement import Cephalo_Measurement
from app.schemas.cephalo_measurement import MeasurementCreate, MeasurementUpdate

from app.nn_models.cephalo import cephaloConstants
from app.crud.crud_cephalo_landmark import landmark

class CRUDMeasurement(CRUDBase[Cephalo_Measurement, MeasurementCreate, MeasurementUpdate]):
    def create_with_cephalo(
        self, db:Session, *, cephalo_id: int
    ) -> Cephalo_Measurement:
        new_measurement = ""
        landmarks_dict = {}

        # get all landmarks for cephalo_id
        for instance in landmark.get_landmarks_by_cephalo(db=db, cephalo_id=cephalo_id):
            landmarks_dict[instance.landmark_number] = [instance.landmark_x, instance.landmark_y]
        print(landmarks_dict)

        for measurement_points in cephaloConstants.angles_list:
            if cephaloConstants.can_calculate_measurement(measurement_points):
                landmark_ids = []
                measurement_value = 0
                for x in measurement_points:
                    landmark_ids.extend(cephaloConstants.acronym_to_landmark_ids(x))
                print(landmark_ids)

                if len(landmark_ids) == 3:
                    measurement_value = cephaloConstants.angle_between_three_points(landmarks_dict[landmark_ids[0]], landmarks_dict[landmark_ids[1]], landmarks_dict[landmark_ids[2]])
                    measurement_value = round(measurement_value, 1)
                else:
                    measurement_value = cephaloConstants.calculate_angle(measurement_points)

                print(measurement_value)
                new_measurement = MeasurementCreate(measurement_name="-".join(measurement_points), unit="deg", value=measurement_value)
                break
        #
        # for measurement_points in cephaloConstants.distance_list:
        #     if cephaloConstants.can_calculate_measurement(measurement_points):
        #         measurement_value = cephaloConstants.calculate_distance(measurement_points)
        #         new_measurement = schemas.MeasurementCreate(measurement_name="-".join(measurement_points), unit="mm", value="10")
        #         crud.measurement.create_with_cephalo(db=db, obj_in=new_measurement, cephalo_id=cephalo_id)
        # new_measurement = MeasurementCreate(measurement_name="asd", value="10", unit="deg")
        print(new_measurement)
        obj_in_data = jsonable_encoder(new_measurement)
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
