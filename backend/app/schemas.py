from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DishBase(BaseModel):
    dishName: str
    imageUrl: str
    isPublished: bool = False

class DishCreate(DishBase):
    pass

class DishResponse(DishBase):
    dishId: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
