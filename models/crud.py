from sqlalchemy.orm import Session
from . import user as user_model, food_entry as food_model, goal as goal_model
from datetime import date

# User CRUD operations
def create_user(db: Session, name: str):
    db_user = user_model.User(name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_name(db: Session, name: str):
    return db.query(user_model.User).filter(user_model.User.name == name).first()

# FoodEntry CRUD operations
def create_food_entry(db: Session, user_id: int, food: str, calories: int, entry_date: date):
    db_entry = food_model.FoodEntry(
        user_id=user_id,
        food=food,
        calories=calories,
        date=entry_date
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# Goal CRUD operations
def create_goal(db: Session, user_id: int, daily: int, weekly: int):
    db_goal = goal_model.Goal(
        user_id=user_id,
        daily=daily,
        weekly=weekly
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal