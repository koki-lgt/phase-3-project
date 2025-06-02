import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
from models.user import User
from models.food_entry import FoodEntry

# Fixture: in-memory DB session
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

def test_create_food_entry(db_session):
    # Create a user
    user = User(name="Charlie")
    db_session.add(user)
    db_session.commit()

    # Add food entry
    entry = FoodEntry(
        food="Banana",
        calories=100,
        date=date(2025, 6, 1),
        user_id=user.id
    )
    db_session.add(entry)
    db_session.commit()

    # Retrieve entry
    result = db_session.query(FoodEntry).filter_by(food="Banana").first()
    assert result is not None
    assert result.calories == 100
    assert result.user.name == "Charlie"
    assert repr(result) == "<FoodEntry(id=1, food='Banana', calories=100)>"

def test_food_entry_user_relationship(db_session):
    user = User(name="Dana")
    db_session.add(user)
    db_session.commit()

    entry1 = FoodEntry(food="Apple", calories=80, date=date.today(), user_id=user.id)
    entry2 = FoodEntry(food="Orange", calories=90, date=date.today(), user_id=user.id)

    db_session.add_all([entry1, entry2])
    db_session.commit()

    user_from_db = db_session.query(User).filter_by(name="Dana").first()
    assert len(user_from_db.food_entries) == 2
    foods = [fe.food for fe in user_from_db.food_entries]
    assert "Apple" in foods and "Orange" in foods
