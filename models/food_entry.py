from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class FoodEntry(Base):
    __tablename__ = "food_entries"
    id = Column(Integer, primary_key=True, index=True)
    food = Column(String, index=True)
    calories = Column(Integer)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="food_entries")
    def __repr__(self):
        return f"<FoodEntry(id={self.id}, food='{self.food}', calories={self.calories})>"