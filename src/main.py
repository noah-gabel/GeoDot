from app import App
from game_manager import Manager
from database import Database
from config import DATABASE_PATH


if __name__ == "__main__":
    app = App(Manager(Database(DATABASE_PATH)))
    app.start()