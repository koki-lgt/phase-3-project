import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
from models.user import User

# Fixture: In-memory SQLite DB session
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

def test_create_user(db_session):
    user = User(name="Alice")
    db_session.add(user)
    db_session.commit()

    retrieved = db_session.query(User).filter_by(name="Alice").first()
    assert retrieved is not None
    assert retrieved.name == "Alice"
    assert repr(retrieved) == f"<User(id={retrieved.id}, name='Alice')>"

def test_unique_user_name_constraint(db_session):
    user1 = User(name="Bob")
    user2 = User(name="Bob")
    db_session.add(user1)
    db_session.commit()

    db_session.add(user2)
    with pytest.raises(Exception):  # likely IntegrityError depending on DB backend
        db_session.commit()

def test_user_relationships_default_empty(db_session):
    user = User(name="Charlie")
    db_session.add(user)
    db_session.commit()

    retrieved = db_session.query(User).filter_by(name="Charlie").first()
    assert retrieved.food_entries == []
    assert retrieved.meal_plans == []
    assert retrieved.goals is None
