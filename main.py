import click
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.models.food_entry import FoodEntry
from app.models.goal import Goal
from app.models.meal_plan import MealPlan
from app import crud  # Assuming crud.py is in app/

# Helper: get DB session and close after use
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@click.group()
def cli():
    """Health app CLI commands."""
    pass

# -------- User Commands --------

@cli.group()
def user():
    """User management commands."""
    pass

@user.command("create")
@click.option('--name', prompt=True, help="Name of the user")
def create_user(name):
    db = next(get_db())
    existing = crud.get_user_by_name(db, name)
    if existing:
        click.echo(f"User '{name}' already exists.")
        return
    user = crud.create_user(db, name)
    click.echo(f"Created user: {user}")

@user.command("list")
def list_users():
    db = next(get_db())
    users = crud.get_users(db)
    for u in users:
        click.echo(f"ID: {u.id}, Name: {u.name}")

# -------- Food Entry Commands --------

@cli.group()
def entry():
    """Food entry commands."""
    pass

@entry.command("add")
@click.option('--user', 'username', required=True, help="User's name")
@click.option('--food', required=True, help="Food item")
@click.option('--calories', required=True, type=int, help="Calories")
@click.option('--date', required=True, help="Date YYYY-MM-DD")
def add_entry(username, food, calories, date):
    db = next(get_db())
    user = crud.get_user_by_name(db, username)
    if not user:
        click.echo(f"User '{username}' not found.")
        return
    entry = crud.create_food_entry(db, user.id, food, calories, date)
    click.echo(f"Added entry: {entry}")

@entry.command("list")
@click.option('--user', 'username', default=None, help="Filter by user name")
@click.option('--date', default=None, help="Filter by date YYYY-MM-DD")
def list_entries(username, date):
    db = next(get_db())
    user_id = None
    if username:
        user = crud.get_user_by_name(db, username)
        if not user:
            click.echo(f"User '{username}' not found.")
            return
        user_id = user.id
    entries = crud.get_food_entries(db, user_id=user_id, date=date)
    for e in entries:
        click.echo(f"ID: {e.id}, Food: {e.food}, Calories: {e.calories}, Date: {e.date}, User ID: {e.user_id}")

# You can add more commands similarly for update/delete entry, goals, meal plans, etc.

if __name__ == '__main__':
    cli()
