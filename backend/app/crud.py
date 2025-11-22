from sqlalchemy.orm import Session
from app.models import Dish
from app.schemas import DishCreate

def get_all_dishes(db: Session):
    return db.query(Dish).order_by(Dish.dishId).all()

def get_dish_by_id(db: Session, dish_id: int):
    return db.query(Dish).filter(Dish.dishId == dish_id).first()

def toggle_dish_status(db: Session, dish_id: int):
    dish = get_dish_by_id(db, dish_id)
    if dish:
        dish.isPublished = not dish.isPublished
        db.commit()
        db.refresh(dish)
    return dish

def create_dish(db: Session, dish: DishCreate):
    db_dish = Dish(**dish.dict())
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish
