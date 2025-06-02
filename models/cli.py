# models/cli.py
import click
from datetime import datetime
from .database import SessionLocal
from .user import User
from .food_entry import FoodEntry
from .crud import create_user, get_user_by_name, add_food_entry, list_users, list_food_entries

# Initialize the Click command group
@click.group()
def cli():
    """Health Simplified CLI Application"""
    pass

# User command group
@cli.group()
def user():
    """Manage users"""
    pass

@user.command()
@click.option('--name', required=True, help='Name of the user')
def create(name):
    """Create a new user"""
    with SessionLocal() as session:
        user = get_user_by_name(session, name)
        if user:
            click.echo(f"User {name} already exists")
        else:
            create_user(session, name)
            click.echo(f"Created user {name}")

@user.command()
def list():
    """List all users"""
    with SessionLocal() as session:
        users = list_users(session)
        if not users:
            click.echo("No users found")
            return
            
        click.echo("Users:")
        for user in users:
            click.echo(f"- {user.name}")

# Entry command group
@cli.group()
def entry():
    """Manage food entries"""
    pass

@entry.command()
@click.option('--user', required=True, help='User name')
@click.option('--food', required=True, help='Food name')
@click.option('--calories', required=True, type=int, help='Calorie count')
@click.option('--date', default=datetime.today().strftime('%Y-%m-%d'), 
              help='Date in YYYY-MM-DD format')
def add(user, food, calories, date):
    """Add a new food entry"""
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        click.echo("Invalid date format. Use YYYY-MM-DD")
        return

    with SessionLocal() as session:
        db_user = get_user_by_name(session, user)
        if not db_user:
            click.echo(f"User {user} not found")
            return
            
        add_food_entry(
            session,
            food=food,
            calories=calories,
            date=date_obj,
            user_id=db_user.id
        )
        click.echo(f"Added entry: {food} ({calories} cal) on {date}")

@entry.command()
@click.option('--user', help='Filter by user name')
@click.option('--date', help='Filter by date (YYYY-MM-DD)')
def list(user, date):
    """List food entries"""
    with SessionLocal() as session:
        # Handle date filter
        date_obj = None
        if date:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                click.echo("Invalid date format. Use YYYY-MM-DD")
                return
                
        # Handle user filter
        user_id = None
        if user:
            db_user = get_user_by_name(session, user)
            if not db_user:
                click.echo(f"User {user} not found")
                return
            user_id = db_user.id
        
        entries = list_food_entries(session, user_id=user_id, date=date_obj)
        
        if not entries:
            click.echo("No entries found")
            return
            
        click.echo("Food Entries:")
        for entry in entries:
            user_name = get_user_by_name(session, id=entry.user_id).name
            click.echo(f"- {entry.date}: {user_name} ate {entry.food} ({entry.calories} cal)")