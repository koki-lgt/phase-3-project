import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
from models.user import User
from models.goal import Goal

# Fixture: in-memory test database session
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

def test_create_goal(db_session):
    # Create a user
    user = User(name="Eve")
    db_session.add(user)
    db_session.commit()

    # Create a goal linked to the user
    goal = Goal(daily=2000, weekly=14000, user_id=user.id)
    db_session.add(goal)
    db_session.commit()

    result = db_session.query(Goal).filter_by(daily=2000).first()
    assert result is not None
    assert result.weekly == 14000
    assert result.user.name == "Eve"
    assert repr(result) == "<Goal(id=1, daily=2000, weekly=14000)>"

def test_user_goal_relationship(db_session):
    user = User(name="Frank")
    goal = Goal(daily=1800, weekly=12600)
    user.goals = goal  # one-to-one relationship

    db_session.add(user)
    db_session.commit()

    user_from_db = db_session.query(User).filter_by(name="Frank").first()
    assert user_from_db.goals is not None
    assert user_from_db.goals.daily == 1800
    assert user_from_db.goals.weekly == 12600
