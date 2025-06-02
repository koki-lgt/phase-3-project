import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
from models.user import User
from models.meal_plan import MealPlan

# Fixture: in-memory SQLite session
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_create_meal_plan(db_session):
    user = User(name="Grace")
    db_session.add(user)
    db_session.commit()

    meal_plan = MealPlan(
        day="Monday",
        meal="Breakfast - Oatmeal",
        calories=350,
        user_id=user.id
    )
    db_session.add(meal_plan)
    db_session.commit()

    result = db_session.query(MealPlan).filter_by(day="Monday").first()
    assert result is not None
    assert result.meal == "Breakfast - Oatmeal"
    assert result.calories == 350
    assert result.user.name == "Grace"
    assert repr(result) == "<MealPlan(id=1, day='Monday', meal='Breakfast - Oatmeal')>"

def test_user_meal_plan_relationship(db_session):
    user = User(name="Henry")
    meal1 = MealPlan(day="Tuesday", meal="Lunch - Salad", calories=400)
    meal2 = MealPlan(day="Wednesday", meal="Dinner - Pasta", calories=600)
    user.meal_plans = [meal1, meal2]

    db_session.add(user)
    db_session.commit()

    user_from_db = db_session.query(User).filter_by(name="Henry").first()
    assert len(user_from_db.meal_plans) == 2
    meals = [m.meal for m in user_from_db.meal_plans]
    assert "Lunch - Salad" in meals
    assert "Dinner - Pasta" in meals
