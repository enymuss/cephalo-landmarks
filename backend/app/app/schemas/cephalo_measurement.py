from typing import Optional

from pydantic import BaseModel

#Shared properties
class MeasurementBase(BaseModel):
    measurement_name: Optional[str] = None
    unit: Optional[str] = None
    value: Optional[float] = None

# Properties to receive on landmark creation
class MeasurementCreate(MeasurementBase):
    measurement_name: str
    unit: str
    value: float

# Properties to receive on landmark update
class MeasurementUpdate(MeasurementBase):
    pass

# Properties shared by models stored in DB
class MeasurementInDBBase(MeasurementBase):
    id: int
    measurement_name: str
    unit: str
    value: float
    cephalo_id: int

    class Config:
        orm_mode = True

# Properties to return to client
class Measurement(MeasurementInDBBase):
    pass

# Properties stored in DB
class MeasurementInDB(MeasurementInDBBase):
    pass
