from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    daily = Column(Integer)
    weekly = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="goals")
    def __repr__(self):
        return f"<Goal(id={self.id}, daily={self.daily}, weekly={self.weekly})>"