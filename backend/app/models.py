from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Dish(Base):
    __tablename__ = "dishes"

    dishId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dishName = Column(String(255), nullable=False)
    imageUrl = Column(Text, nullable=False)
    isPublished = Column(Boolean, default=False, nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
