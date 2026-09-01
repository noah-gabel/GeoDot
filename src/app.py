import customtkinter as ctk
from game_manager import Manager
from ui.game import GameScreen
from config import FG_COLOR

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

        GameScreen(master=self, round=self.round, current_score=self.current_score, current_city=self.current_city, guess_action=self._guess).show()
        

    def _guess(self):
        print("clicked")

    def start(self):
        self.mainloop()
