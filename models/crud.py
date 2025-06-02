# models/crud.py
from sqlalchemy.orm import Session
from .user import User
from .food_entry import FoodEntry

def create_user(session: Session, name: str):
    """Create a new user"""
    new_user = User(name=name)
    session.add(new_user)
    session.commit()
    return new_user

def get_user_by_name(session: Session, name: str = None, id: int = None):
    """Get user by name or ID"""
    if name:
        return session.query(User).filter(User.name == name).first()
    if id:
        return session.query(User).filter(User.id == id).first()
    return None

def list_users(session: Session):
    """List all users"""
    return session.query(User).all()

def add_food_entry(session: Session, food: str, calories: int, date, user_id: int):
    """Add a new food entry"""
    new_entry = FoodEntry(
        food=food,
        calories=calories,
        date=date,
        user_id=user_id
    )
    session.add(new_entry)
    session.commit()
    return new_entry

def list_food_entries(session: Session, user_id: int = None, date = None):
    """List food entries with optional filters"""
    query = session.query(FoodEntry)
    
    if user_id:
        query = query.filter(FoodEntry.user_id == user_id)
        
    if date:
        query = query.filter(FoodEntry.date == date)
        
    return query.all()