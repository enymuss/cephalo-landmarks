from typing import Optional

from pydantic import BaseModel

#Shared properties
class LandmarkBase(BaseModel):
    landmark_number: Optional[int] = None
    landmark_x: Optional[float] = None
    landmark_y: Optional[float] = None

# Properties to receive on landmark creation
class LandmarkCreate(LandmarkBase):
    landmark_number: int
    landmark_x: float
    landmark_y: float

# Properties to receive on landmark update
class LandmarkUpdate(LandmarkBase):
    pass

# Properties shared by models stored in DB
class LandmarkInDBBase(LandmarkBase):
    id: int
    landmark_number: int
    landmark_x: float
    landmark_y: float
    cephalo_id: int

    class Config:
        orm_mode = True

# Properties to return to client
class Landmark(LandmarkInDBBase):
    pass

# Properties stored in DB
class LandmarkInDB(LandmarkInDBBase):
    pass
