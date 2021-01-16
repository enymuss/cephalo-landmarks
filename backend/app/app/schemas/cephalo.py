from typing import Optional

from pydantic import BaseModel

#Shared Properties
class CephaloBase(BaseModel):
    file_path: Optional[str] = None
    px_per_cm: Optional[int] = None

# Properties to receive on cephalo item creation
class CephaloCreate(CephaloBase):
    file_path: string
    px_per_cm: int

# Properties to receive on cephalo item update
class CephaloUpdate(CephaloBase):
    pass

# Properties shared by models stored in db
class CephaloInDBBase(CephaloBase):
    id: int
    file_path: string
    px_per_cm: int

    class Config:
        orm_mode = True

# Properties to return via API
class Cephalo(CephaloInDBBase):
    pass


# Properties stored in DB
class CephaloInDB(CephaloInDB):
    pass
