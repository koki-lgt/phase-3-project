import pytest
from datetime import date
from sqlalchemy.orm import Session
from health_simplified.database import Base, engine, SessionLocal
from health_simplified.crud import *

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.rollback()
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_user_crud(db_session: Session):
    # Create
    user = create_user(db_session, "Test User")
    assert user.id is not None
    
    # Read
    found = get_user_by_name(db_session, "Test User")
    assert found.id == user.id
    
    # Update
    updated = update_user(db_session, user.id, "Updated User")
    assert updated.name == "Updated User"
    
    # Delete
    assert delete_user(db_session, user.id) is True
    assert get_user_by_name(db_session, "Updated User") is None

def test_food_entry_crud(db_session: Session):
    user = create_user(db_session, "Food User")
    entry = create_food_entry(db_session, user.id, "Apple", 95, date(2023, 1, 1))
    
    # Update
    updated = update_food_entry(db_session, entry.id, calories=100)
    assert updated.calories == 100
    
    # Delete
    assert delete_food_entry(db_session, entry.id) is True

def test_goal_crud(db_session: Session):
    user = create_user(db_session, "Goal User")
    goal = create_goal(db_session, user.id, 2000, 14000)
    
    # Update
    updated = update_goal(db_session, goal.id, weekly=15000)
    assert updated.weekly == 15000

def test_relationships(db_session: Session):
    user = create_user(db_session, "Relation User")
    
    # FoodEntry relationship
    entry = create_food_entry(db_session, user.id, "Banana", 105, date.today())
    assert entry in user.food_entries
    
    # Goal relationship
    goal = create_goal(db_session, user.id, 2000, 14000)
    assert user.goals == goal
    
    # MealPlan relationship
    plan = create_meal_plan(db_session, user.id, "Monday", "Breakfast", 300)
    assert plan in user.meal_plans