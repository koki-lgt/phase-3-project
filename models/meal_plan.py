from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class MealPlan(Base):
    __tablename__ = 'meal_plans'
    id = Column(Integer, primary_key=True, index=True)
    day = Column(String, nullable=False)
    meal = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="meal_plans")
    
    # FIXED: Proper __repr__ method without syntax error
    def __repr__(self):
        return f"<MealPlan(id={self.id}, day='{self.day}', meal='{self.meal}')>"