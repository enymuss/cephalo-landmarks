import inspect
from typing import Optional, Type

from fastapi import Form

from pydantic import BaseModel

def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls

#Shared Properties
class CephaloBase(BaseModel):
    px_per_cm: Optional[int] = None

# Properties to receive on cephalo item creation
@as_form
class CephaloCreate(CephaloBase):
    px_per_cm: int

# Properties to receive on cephalo item update
class CephaloUpdate(CephaloBase):
    pass

# Properties shared by models stored in db
class CephaloInDBBase(CephaloBase):
    id: int
    px_per_cm: int

    class Config:
        orm_mode = True

# Properties to return via API
class Cephalo(CephaloInDBBase):
    pass

# Properties stored in DB
class CephaloInDB(CephaloInDBBase):
    file_path: str
    pass
