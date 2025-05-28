import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from datetime import date
from sqlalchemy.orm import Session
from models.database import Base, engine, SessionLocal
from models.crud import *

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.rollback()
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_user_crud(db_session):
    # Create
    user = create_user(db_session, "Test User")
    assert user.id is not None
    
    # Read
    found = get_user_by_name(db_session, "Test User")
    assert found.id == user.id
    
    # Update
    updated_user = update_user(db_session, user.id, "Updated User")
    assert updated_user.name == "Updated User"
    
    # Verify update
    found_updated = get_user_by_name(db_session, "Updated User")
    assert found_updated.id == user.id
    
    # Delete
    assert delete_user(db_session, user.id) is True
    assert get_user_by_name(db_session, "Updated User") is None

def test_food_entry_crud(db_session):
    # Create user and entry
    user = create_user(db_session, "Food User")
    entry = create_food_entry(db_session, user.id, "Apple", 95, date(2023, 1, 1))
    
    # Update
    updated_entry = update_food_entry(db_session, entry.id, name="Green Apple", calories=100)
    assert updated_entry.name == "Green Apple"
    assert updated_entry.calories == 100
    
    # Delete
    assert delete_food_entry(db_session, entry.id) is True
    assert get_food_entry_by_id(db_session, entry.id) is None

def test_goal_crud(db_session):
    # Create user and goal
    user = create_user(db_session, "Goal User")
    goal = create_goal(db_session, user.id, daily=2000, weekly=14000)
    
    # Update
    updated_goal = update_goal(db_session, goal.id, weekly=15000)
    assert updated_goal.weekly == 15000
    
    # Test daily remains unchanged
    assert updated_goal.daily == 2000

def test_relationships(db_session):
    # Create user
    user = create_user(db_session, "Relation User")
    
    # FoodEntry relationship
    entry = create_food_entry(db_session, user.id, "Banana", 105, date.today())
    assert entry in user.food_entries
    
    # Goal relationship
    goal = create_goal(db_session, user.id, daily=2000, weekly=14000)
    assert goal in user.goals  # Changed to plural since user can have multiple goals
    
    # MealPlan relationship
    plan = create_meal_plan(db_session, user.id, "Monday", "Breakfast", 300)
    assert plan in user.meal_plans