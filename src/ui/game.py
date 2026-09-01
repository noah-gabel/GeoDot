import customtkinter as ctk
from tkintermapview import TkinterMapView
from config import API_KEY, FG_COLOR, FONT, HEADING_TEXT_COLOR, GUESS_BUTTON_DISABLED_FG_COLOR, GUESS_BUTTON_FG_COLOR, GUESS_BUTTON_HOVER_FG_COLOR
from ui.map_controller import MapController
from models import Guess, City, Coordinates, Difficulty
class GameScreen(ctk.CTkFrame):
    def __init__(self, master, round: ctk.StringVar, current_city: ctk.StringVar, current_score : ctk.IntVar, guess_action):
        super().__init__(master, fg_color=FG_COLOR)

        # define StringVars and IntVars which update according to the parents variables
        self.round = round
        self.current_city = current_city
        self.current_score = current_score

        # define guess button callback
        self.guess_action = guess_action

        self._setup_ui()

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.grid_columnconfigure(0, weight=1)

        self._setup_map_widget()
        self._setup_top_hud()
        self._setup_bottom_hud()

    def _setup_map_widget(self):
        self.map = MapController(self, disable_guess_button=self._disable_guess_button, enable_guess_button=self._enable_guess_button)
        self.map.show_grid(row=1, column=0)

    def _setup_top_hud(self):
        #background frame
        top_bar = ctk.CTkFrame(self, fg_color=FG_COLOR, height=75)
        top_bar.grid(row=0, column=0, sticky="ew", padx=100)

        top_bar.grid_propagate(False)

        top_bar.grid_rowconfigure(0, weight=1)

        top_bar.grid_columnconfigure(0, weight=1)
        top_bar.grid_columnconfigure(1, weight=1)
        top_bar.grid_columnconfigure(2, weight=1)
        top_bar.grid_columnconfigure(3, weight=1)
        top_bar.grid_columnconfigure(4, weight=1)
        top_bar.grid_columnconfigure(5, weight=1)
        top_bar.grid_columnconfigure(6, weight=1)

        #display current round
        round_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        round_frame.grid(row=0, column=1)
        ctk.CTkLabel(round_frame, text="ROUND", text_color=HEADING_TEXT_COLOR, font=(FONT, 10, "bold")).pack()
        ctk.CTkLabel(round_frame, textvariable=self.round, font=(FONT, 20, "bold")).pack()

        #display city name
        city_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        city_frame.grid(row=0, column=3)
        ctk.CTkLabel(city_frame, text="FIND CITY", font=(FONT, 10, "bold"), text_color=HEADING_TEXT_COLOR).pack()
        ctk.CTkLabel(city_frame, textvariable=self.current_city, font=(FONT, 20, "bold")).pack()

        # display total score
        score_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        score_frame.grid(row=0, column=5)
        ctk.CTkLabel(score_frame, text="SCORE", font=(FONT, 10, "bold"), text_color=HEADING_TEXT_COLOR).pack()
        ctk.CTkLabel(score_frame, textvariable=self.current_score, font=(FONT, 20, "bold")).pack()

    def _setup_bottom_hud(self):
        #background frame
        bottom_bar = ctk.CTkFrame(self, fg_color=FG_COLOR, height=75)
        bottom_bar.grid(row=2, column=0, sticky="ew")
        bottom_bar.pack_propagate(False)

        self.guess_button = ctk.CTkButton(
            bottom_bar,
            corner_radius=25,
            text="Guess",
            font=(FONT, 20, "bold"),
            fg_color=GUESS_BUTTON_DISABLED_FG_COLOR,
            hover_color=GUESS_BUTTON_HOVER_FG_COLOR,
            height=50,
            command=self.guess_action,
            state="disabled")

        self.guess_button.pack(expand=True)

    def _disable_guess_button(self):
        self.guess_button.configure(state="disabled", fg_color=GUESS_BUTTON_DISABLED_FG_COLOR)

    def _enable_guess_button(self):
        self.guess_button.configure(state="normal", fg_color=GUESS_BUTTON_FG_COLOR)


    def show(self):
        self.pack(fill="both", expand=True)