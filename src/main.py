"""Entry point for GeoDot.
 
Builds the database, game manager and main window, then starts the Tk event
loop. Run with ``uv run src/main.py``.
"""

from app import App
from game_manager import Manager
from database import Database
from config import DATABASE_PATH


if __name__ == "__main__":
    app = App(Manager(Database(DATABASE_PATH)))
    app.start()