# Initialize database on startup
from .database import init_db
init_db()
from .cli import cli # Importing the CLI app to ensure it is registered
from .user import User
from .food_entry import FoodEntry
from .goal import Goal
from .meal_plan import MealPlan
