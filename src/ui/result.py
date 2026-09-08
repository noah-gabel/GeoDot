import customtkinter as ctk
from ui.screen import Screen
from models import Guess
from ui.map_controller import MapController
from config import FG_COLOR

class ResultScreen(Screen):
    def __init__(self, master):
        super().__init__(master, fg_color=FG_COLOR)

        self._setup_ui()
        
    def _setup_ui(self):
        self.grid_rowconfigure(6, weight=0)

        self.grid_columnconfigure(1, weight=1)


        self._setup_conclusion_map()

    def _setup_conclusion_map(self):
        self.map = MapController(self, corner_radius=10)
        self.map.show_grid(row=0, column=1)

    def show_result_city_markers(self, results: list[Guess]):
        self.map.place_result_city_markers(results=results)
    