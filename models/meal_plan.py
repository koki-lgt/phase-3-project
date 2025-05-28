from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(String)  # Monday-Sunday
    meal_type = Column(String)  # Breakfast/Lunch/Dinner
    food = Column(String)
    calories = Column(Integer)
    date = Column(Date)   # Date of the meal
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="meal_plans")