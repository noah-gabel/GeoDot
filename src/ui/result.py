import customtkinter as ctk
from ui.screen import Screen
from models import Guess, Difficulty
from ui.map_controller import MapController
from ui.formatting import score_color, format_distance
from config import FG_COLOR, FONT, HEADING_TEXT_COLOR, TEXT_COLOR, CARD_FG_COLOR, TEXT_FAINT_COLOR, CARD_BORDER_COLOR, TEXT_DIM_COLOR, MAX_ROUND_SCORE, BUTTON_FG_COLOR, BUTTON_HOVER_FG_COLOR, CARD_HOVER_FG_COLOR, CARD_SELECT_BORDER_COLOR, RESULT_ENTRY_BAR_HEIGHT

class ResultRow(ctk.CTkFrame):
    def __init__(self, master, index : int,  guess: Guess, on_click, border_width = 2, corner_radius = 12):
        super().__init__(master, fg_color=CARD_FG_COLOR, border_width=border_width, corner_radius=corner_radius, height=RESULT_ENTRY_BAR_HEIGHT)

        self.index = index
        self.guess = guess

        self.on_click = on_click

        self._setup_ui()
        #TODO add bindings in order to display only the clicked guess son the map
        self._bind_recursively(self)

    def _setup_ui(self):
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text=f"{self.index + 1}",
            width=24,
            font=(FONT, 14, "bold"),
            text_color=TEXT_FAINT_COLOR,
            anchor="w"
        ).grid(row=0, column=0, rowspan=2, padx=(16, 10))

        ctk.CTkLabel(
            self,
            text=self.guess.city.name,
            font=(FONT, 16, "bold"),
            text_color=TEXT_COLOR,
            anchor="w",
        ).grid(row=0, column=1, sticky="ew", pady=(10, 0))
 
        ctk.CTkLabel(
            self,
            text=format_distance(self.guess.distance),
            font=(FONT, 14),
            text_color=TEXT_DIM_COLOR,
            anchor="e",
            width=90,
        ).grid(row=0, column=2, sticky="e", padx=10, pady=(10, 0))
 
        ctk.CTkLabel(
            self,
            text=f"{self.guess.score} pts",
            font=(FONT, 16, "bold"),
            text_color=score_color(self.guess.score),
            anchor="e",
            width=90,
        ).grid(row=0, column=3, sticky="e", padx=(10, 16), pady=(10, 0))
 
        bar = ctk.CTkProgressBar(
            self,
            height=4,
            corner_radius=2,
            fg_color=CARD_BORDER_COLOR,
            progress_color=score_color(self.guess.score),
        )
        bar.set(self.guess.score / MAX_ROUND_SCORE)
        bar.grid(row=1, column=1, columnspan=3, sticky="ew", padx=(0, 16), pady=(6, 12))

    def _bind_recursively(self, widget):
        widget.bind("<Button-1>", self._on_click, add="+")
        widget.bind("<Enter>", self._on_enter, add="+")
        widget.bind("<Leave>", self._on_exit, add="+")

        for child in widget.winfo_children():
            self._bind_recursively(child)

    def _on_click(self, _event):
        self.on_click(self, self.index)

        # return "break" to stop tkinter from passing the event to the parent and prevent double registers for one click
        return "break"

    def _on_enter(self, _event):
        self.configure(fg_color=CARD_HOVER_FG_COLOR)
        self.configure(cursor="hand2")

    def _on_exit(self, _event):
        self.configure(fg_color=CARD_FG_COLOR)
        self.configure(cursor="")


class ResultScreen(Screen):
    def __init__(self, master, total_score, play_again, change_difficulty):
        super().__init__(master, fg_color=FG_COLOR)

        #define button callbacks
        self.play_again = play_again
        self.change_difficulty = change_difficulty

        self.total_score = total_score

        self.difficulty: None | Difficulty = None
        self.results: list[Guess] = []
        self.result_row: ResultRow | None = None

        self._setup_ui()
        
    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure(3, weight=0)

        self._setup_header()
        self._setup_map()
        self._setup_result_list()
        self._setup_buttons()

    def _setup_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=1, pady=(20, 12))
 
        ctk.CTkLabel(
            header,
            text="FINAL SCORE",
            font=(FONT, 12, "bold"),
            text_color=HEADING_TEXT_COLOR,
        ).pack()
 
        ctk.CTkLabel(
            header,
            textvariable=self.total_score,
            font=(FONT, 44, "bold"),
            text_color=TEXT_COLOR,
        ).pack()

    def _setup_map(self):
        self.map = MapController(self, corner_radius=10, allow_guessing=False)
        self.map.grid(row=1, column=1, sticky="nswe", padx=60, pady=(0, 12))

    def _setup_result_list(self):
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_fg_color="transparent", scrollbar_button_color=FG_COLOR, scrollbar_button_hover_color=FG_COLOR)
        self.list_frame.grid(row=2, column=1, sticky="nswe", padx=60)

        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(1, weight=0)
        self.list_frame.grid_columnconfigure(2, weight=1)

    def _setup_buttons(self):
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=1, pady=25)

        ctk.CTkButton(
            button_frame,
            text="Play again",
            font=(FONT, 18, "bold"),
            corner_radius=30,
            height=55,
            width=240,
            fg_color=BUTTON_FG_COLOR,
            hover_color=BUTTON_HOVER_FG_COLOR,
            command=self.play_again,
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Change difficulty",
            font=(FONT, 18, "bold"),
            corner_radius=30,
            height=55,
            width=240,
            fg_color="transparent",
            border_width=2,
            border_color=CARD_BORDER_COLOR,
            hover_color=CARD_HOVER_FG_COLOR,
            text_color=TEXT_COLOR,
            command=self.change_difficulty,
        ).pack(side="left", padx=10)

    def reset(self, difficulty: Difficulty):
        self.map.reset(difficulty=difficulty)

        self.difficulty = None
        self.results = []
        self.result_row = None

    def _result_row_clicked(self, widget, index: int):
        if self.difficulty is None:
            return
        self.map.reset(difficulty=self.difficulty)

        if widget is self.result_row:
            self.result_row = None

            widget.configure(border_color = CARD_BORDER_COLOR)
            self.map.place_result_city_markers(results=self.results)
        else:
            if self.result_row is not None:
                self.result_row.configure(border_color = CARD_BORDER_COLOR)

            self.result_row = widget
            widget.configure(border_color = CARD_SELECT_BORDER_COLOR)

            guess = self.results[index]
            self.map.place_guess_city_combo(guess=guess)

    def show_results(self, results: list[Guess], difficulty: Difficulty):
        self.difficulty = difficulty
        self.results = results

        self.map.place_result_city_markers(results=self.results)

        for index, guess in enumerate(results):
            result_frame = ResultRow(self.list_frame, index=index, guess=guess, on_click=self._result_row_clicked)
            result_frame.grid(row=index, column=0, sticky="ew", pady=4, columnspan=3)
    