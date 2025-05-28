from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Relationships
    food_entries = relationship("FoodEntry", back_populates="user")
    goals = relationship("Goal", back_populates="user", uselist=False)
    meal_plans = relationship("MealPlan", back_populates="user")