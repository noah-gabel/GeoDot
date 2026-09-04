import customtkinter as ctk
from game_manager import Manager
from ui.game import GameScreen
from ui.start import MenuScreen
from config import FG_COLOR
from models import Coordinates, Difficulty

class App(ctk.CTk):

    def __init__(self, game_manager: Manager, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color=FG_COLOR)
        self.game_manager = game_manager
        self.title("GeoDot")

        # change the window to fullscreen
        # delay is needed in order for it to work
        self.after(1, lambda: self.state("zoomed"))
        

        self.current_city = ctk.StringVar(value="N/A")
        self.round = ctk.StringVar(value="N/A")
        self.current_score = ctk.IntVar(value=0)

        self.game_manager.start_game(difficulty=Difficulty.HARD)

        self.screen = GameScreen(master=self, round=self.round, current_score=self.current_score, current_city=self.current_city, guess_action=self._show_round_results)
        self.menu = MenuScreen(self, "test")
        self.menu.show()

    def _show_round_results(self):
        print("clicked")
        coordinates = self.screen.get_guess_coords()
        if coordinates is None:
            return
        
        coordinates = Coordinates(lat=coordinates.lat, lon=coordinates.lon)
        self.game_manager.submit_guess(coordinates=coordinates)
    
    def start(self):
        self.mainloop()
