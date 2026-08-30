from app import App
from game_manager import Manager
from database import Database


if __name__ == "__main__":
    app = App(Manager(Database("./terra.sqlite")))
    app.start()