import customtkinter as ctk
from config import (FG_COLOR, FONT, INTRO_HEADING_ACCENT_COLOR, TEXT_COLOR, TEXT_DIM_COLOR, HEADING_TEXT_COLOR, CARD_BORDER_COLOR, CARD_FG_COLOR, GERMANY_DIFFICULTY_COLOR, EUROPE_DIFFICULTY_COLOR, WORLDWIDE_DIFFICULTY_COLOR, CARD_INNER_PADX, CARD_WIDTH, UNSELECTED_DIFFICULTY_COLOR)
from models import Difficulty

class MenuScreen(ctk.CTkFrame):
    def __init__(self, master, start_game):
        super().__init__(master, fg_color=FG_COLOR, )

        self._setup_ui()

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # configuring row 0 and 6 with weight 1 to push the main info to teh center
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self._setup_heading()
        self._setup_difficulty_cards()

    def _setup_heading(self):
        title = ctk.CTkFrame(self, fg_color="transparent")
        title.grid(row=1, column=0, pady=(0, 8))

        # separate the title in order to color only the Dot part
        ctk.CTkLabel(
            title, 
            text="Geo", 
            font=(FONT, 52, "bold"), 
            text_color=TEXT_COLOR, 
            padx=0 
        ).pack(side="left")
        ctk.CTkLabel(
            title, 
            text="Dot", 
            font=(FONT, 52, "bold"), 
            text_color=INTRO_HEADING_ACCENT_COLOR, 
            padx=0, 
        ).pack(side="left")

        # description
        ctk.CTkLabel( 
            self, 
            text="place your marker as close as you can to the asked city", 
            font=(FONT, 15), 
            text_color=TEXT_DIM_COLOR 
        ).grid(row=2, column=0, pady=(0, 40))

        # difficulty cards heading
        ctk.CTkLabel(
            self, 
            text="DIFFICULTY", 
            font=(FONT, 20, "bold"),
            text_color=HEADING_TEXT_COLOR 
        ).grid(row=3, column=0, pady=(0, 12))

    def _setup_difficulty_cards(self):
        card_frame = ctk.CTkFrame(self, fg_color="transparent")
        card_frame.grid(row=4, column=0)

        card_frame.grid_rowconfigure(0, weight=1)
        card_frame.grid_columnconfigure(len(Difficulty) - 1)

        for index, difficulty, in enumerate(Difficulty):
            DifficultyCard(card_frame, difficulty=difficulty, on_click="").grid(row=0, column=index, padx=10)

    def show(self):
        self.pack(fill="both", expand=True)

class DifficultyCard(ctk.CTkFrame):
    def __init__(self, master, difficulty: Difficulty, on_click, border_width=1, corner_radius=10):
        super().__init__(master=master, fg_color=CARD_FG_COLOR, border_color=CARD_BORDER_COLOR, border_width=border_width, corner_radius=corner_radius)

        self.difficulty = difficulty

        self._setup_ui()

    def _setup_ui(self):
        self.grid_propagate(False)

        #set texts according to difficulty level
        match self.difficulty:
            case Difficulty.EASY:
                title = "Easy"
                scope = "GERMANY"
                scope_color = GERMANY_DIFFICULTY_COLOR
                description = "Only metropolises from inside Germany with more than 500.000 citizens"
                level = 1
            case Difficulty.STANDARD:
                title = "Standard"
                scope = "GERMANY"
                scope_color = GERMANY_DIFFICULTY_COLOR
                description = "Every German city with more than 50.000 citizens"
                level = 2
            case Difficulty.HARD:
                title = "Hard"
                scope = "EUROPE"
                scope_color = EUROPE_DIFFICULTY_COLOR
                description = "Cities in Europe with more than 300.000 citizens"
                level = 3
            case Difficulty.EXTREME:
                title = "Extreme"
                scope = "EUROPE"
                scope_color = EUROPE_DIFFICULTY_COLOR
                description = "European cities with more than 50.000 citizens"
                level = 4
            case Difficulty.IMPOSSIBLE:
                title = "Impossible"
                scope = "WORLDWIDE"
                scope_color = WORLDWIDE_DIFFICULTY_COLOR
                description = "Every city in the world with more than 50.000 citizens"
                level = 5
            case _:
                raise ValueError("Difficulty does not match pattern")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._setup_difficulty_bar(level=level, scope_color=scope_color)
        self._setup_text(scope_color=scope_color, scope=scope, title=title, description=description)

    def _setup_difficulty_bar(self, level: int, scope_color:str):
        bar_frame = ctk.CTkFrame(self, fg_color="transparent", width=CARD_WIDTH)
        bar_frame.grid(row=0, column=0, pady=(15, 5), padx=CARD_INNER_PADX - 3)

        # configure columns for the amount of difficulty levels you have
        for index in range(len(Difficulty)):
            bar_frame.grid_columnconfigure(index, weight=1)

        bar_frame.grid_rowconfigure(0, weight=1)

        # generate the difficulty bar to change the amount of coloured spaces for teh difficulty level
        for index in range(len(Difficulty)):
            if index >= level:
                scope_color = UNSELECTED_DIFFICULTY_COLOR
            print(index)
            ctk.CTkFrame(bar_frame, corner_radius=10, fg_color=scope_color, height=10).grid(row=0, column=index, sticky="ew", padx=3)    

    def _setup_text(self, scope: str, scope_color:str, title: str, description:str):
        ctk.CTkLabel(
            self,
            text=scope,
            font=(FONT, 12, "bold"),
            text_color=scope_color,
            anchor="w",
        ).grid(row=1, column=0, sticky="ew", padx=CARD_INNER_PADX)

        ctk.CTkLabel(
            self,
            text=title,
            font=(FONT, 18, "bold"),
            text_color=TEXT_COLOR,
            anchor="w",
        ).grid(row=2, column=0, sticky="ew", padx=CARD_INNER_PADX, pady=(2, 4))

        ctk.CTkLabel(
            self,
            text=description,
            font=(FONT, 12),
            text_color=TEXT_DIM_COLOR,
            anchor="nw",
            justify="left",
            wraplength= CARD_WIDTH - 2 * CARD_INNER_PADX
        ).grid(row=3, column=0, sticky="new", padx=CARD_INNER_PADX, pady=4)
