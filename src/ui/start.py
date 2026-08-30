import customtkinter as ctk
from config import FG_COLOR

class MenuScreen(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color=FG_COLOR)