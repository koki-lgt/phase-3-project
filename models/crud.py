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

def update_user(db: Session, user_id: int, new_name: str):
    user = db.query(user.User).filter(user.User.id == user_id).first()
    if user:
        user.name = new_name
        db.commit()
        return user
    return None

def delete_user(db: Session, user_id: int):
    user = db.query(user.User).filter(user.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


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

def update_food_entry(db: Session, entry_id: int, **kwargs):
    entry = db.query(food_entry.FoodEntry).filter(food_entry.FoodEntry.id == entry_id).first()
    if entry:
        for key, value in kwargs.items():
            setattr(entry, key, value)
        db.commit()
        return entry
    return None

def delete_food_entry(db: Session, entry_id: int):
    entry = db.query(food_entry.FoodEntry).filter(food_entry.FoodEntry.id == entry_id).first()
    if entry:
        db.delete(entry)
        db.commit()
        return True
    return False


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

    def update_goal(db: Session, goal_id: int, **kwargs):
    goal = db.query(goal.Goal).filter(goal.Goal.id == goal_id).first()
    if goal:
        for key, value in kwargs.items():
            setattr(goal, key, value)
        db.commit()
        return goal
    return None

     # MealPlan CRUD
def create_meal_plan(db: Session, user_id: int, day: str, meal: str, calories: int):
    new_plan = meal_plan.MealPlan(
        user_id=user_id,
        day=day,
        meal=meal,
        calories=calories
    )
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan


