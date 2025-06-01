from pydantic import BaseModel

class PointBase(BaseModel):
    latitude: float
    longitude: float
    description: str

class PointCreate(PointBase):
    pass

class Point(PointBase):
    id: int

    class Config:
        orm_mode = True
        
class PointUpdate(BaseModel):
    latitude: float
    longitude: float
    description: str
