"""In-game screen with the map, the HUD and the per-round result overlay."""

import customtkinter as ctk
from config import FG_COLOR, FONT, HEADING_TEXT_COLOR, GUESS_BUTTON_DISABLED_FG_COLOR, GUESS_BUTTON_FG_COLOR, GUESS_BUTTON_HOVER_FG_COLOR, CARD_BORDER_COLOR, TEXT_COLOR, MAX_ROUND_SCORE, COUNTDOWN_TIME
from ui.map_controller import MapController
from ui.screen import Screen
from ui.formatting import score_color, format_distance
from models import Difficulty, Guess, Coordinates

class RoundResultBar(ctk.CTkFrame):
    """Overlay that reveals a round's score and distance, then counts down.

    When the countdown reaches zero, ``next_round`` is called.

    Args:
        master: Parent widget.
        next_round: Called when the countdown has finished.
    """
    def __init__(self, master, next_round):
        super().__init__(master, fg_color=FG_COLOR)

        self.score = ctk.IntVar(value=0)
        self.countdown = ctk.IntVar(value=COUNTDOWN_TIME)
        self.distance = ctk.StringVar(value="N/A")

        self.next_round = next_round
        self._setup_ui()

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1, uniform="column")
        self.grid_columnconfigure(1, weight=1, uniform="column")
        self.grid_columnconfigure(2, weight=1, uniform="column")

        self._setup_stat(column=0, heading="SCORE", text_variable=self.score, anchor="w")
        self._setup_countdown()
        self._setup_stat(column=2, heading="DISTANCE", text_variable=self.distance, anchor="e")
        self._setup_bar()

    def _setup_stat(self, column: int, heading: str, text_variable: ctk.StringVar | ctk.IntVar, anchor: str):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=0, column=column, sticky="ew", padx=20, pady=(12, 8))
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, 
            text=heading, 
            font=(FONT, 10, "bold"),
            text_color=HEADING_TEXT_COLOR, 
            anchor=anchor
        ).grid(row=0, column=0, sticky="ew")

        label = ctk.CTkLabel(
            frame, 
            textvariable=text_variable, 
            font=(FONT, 22, "bold"),
            text_color=TEXT_COLOR, 
            anchor=anchor)
        label.grid(row=1, column=0, sticky="ew")

    def _setup_countdown(self):
        ctk.CTkLabel(
            self, 
            textvariable=self.countdown, 
            font=(FONT, 40, "bold"),
            text_color=TEXT_COLOR
        ).grid(row=0, column=1, pady=(12, 8))

    def _setup_bar(self):
        self.bar = ctk.CTkProgressBar(self, height=6, corner_radius=3, fg_color=CARD_BORDER_COLOR)
        self.bar.set(0)
        self.bar.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=(0, 14))

    def show(self, guess:Guess):
        """Animate the result of a round and start the countdown after one second.
 
        Args:
            guess: The result to reveal.
        """
        self._animate(guess=guess, current_step=0)
        self.after(1000, self._start_countdown)

    def _animate(self, guess: Guess, current_step: int, steps: int = 30):
        """Count up score, distance and progress bar from zero to the final values.

        Calls itself every 20 ms until ``current_step`` reaches ``steps``.

        Args:
            guess: The result to reveal.
            current_step: The current animation frame, starting at 0.
            steps: Total number of animation frames.
        """
        score: int = round(guess.score * current_step / steps )
        self.score.set(score)

        distance: float = guess.distance * current_step / steps
        self.distance.set(format_distance(distance))

        self.bar.configure(progress_color=score_color(score=score))
        self.bar.set(value=score/ MAX_ROUND_SCORE)

        if current_step < steps:
            current_step += 1
            self.after(20, lambda: self._animate(current_step=current_step, guess=guess, steps=steps))

    def _start_countdown(self):
        """Count down once per second and call ``next_round`` at zero."""
        self.countdown.set(self.countdown.get() - 1)

        if self.countdown.get() > 0:
            self.after(1000, self._start_countdown)
        else:
            self.next_round()

    def reset(self):
        """Hide the overlay and restore its initial values."""
        self.place_forget()

        self.countdown.set(COUNTDOWN_TIME)
        self.score.set(0)
        self.distance.set("N/A")

class GameScreen(Screen):
    """Screen shown while playing: the map, the HUD and the guess button.

    The HUD reads from Tk variables owned by ``App``, so it updates automatically when those change.
 
    Args:
        master: Parent widget.
        rounds: Current round, e.g. ``"3/10"``.
        current_city: Name of the city to find.
        current_score: Total score so far.
        guess_action: Called when the player submits a guess.
        next_round: Called when the result countdown has finished.
    """
    def __init__(self, master, rounds: ctk.StringVar, current_city: ctk.StringVar, current_score : ctk.IntVar, guess_action, next_round):
        super().__init__(master, fg_color=FG_COLOR)

        # define StringVars and IntVars which update according to the parents variables
        self.round = rounds
        self.current_city = current_city
        self.current_score = current_score

        # define callbacks
        self.guess_action = guess_action
        self.next_round = next_round

        self._bind_space_bar()

        self._setup_ui()

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.grid_columnconfigure(0, weight=1)

        self._setup_map_widget()
        self._setup_top_hud()
        self._setup_bottom_hud()

        self.result_bar = RoundResultBar(self, next_round=self.next_round)

    def _setup_map_widget(self):
        self.map = MapController(self, disable_guess_button=self._disable_guess_button, enable_guess_button=self._enable_guess_button)
        self.map.show_grid(row=1, column=0)

    def _setup_top_hud(self):
        top_bar = ctk.CTkFrame(self, fg_color=FG_COLOR, height=75)
        top_bar.grid(row=0, column=0, sticky="ew", padx=100, pady=(0, 10))

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
        ctk.CTkLabel(score_frame, text="TOTAL SCORE", font=(FONT, 10, "bold"), text_color=HEADING_TEXT_COLOR).pack()
        ctk.CTkLabel(score_frame, textvariable=self.current_score, font=(FONT, 20, "bold")).pack()

    def _setup_bottom_hud(self):
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

    def _bind_space_bar(self):
        """Let the space bar submit a guess."""

        # use self.winfo_toplevel to bind it to the toplevel window otherwise the event doesn't fire
        self.winfo_toplevel().bind("<space>", self._submit_space_guess)
        self.focus_set()

    def _submit_space_guess(self, _event):
        if self.guess_button.cget("state") == "disabled":
            return "break"

        self.guess_action()
        return "break"

    def start_round(self, difficulty: Difficulty):
        """Hide the result overlay and reset the map for a new round.

        Args:
            difficulty: Decides the map's default view.
        """
        self.result_bar.reset()
        self.map.reset(difficulty=difficulty)

    def get_guess_coords(self) -> Coordinates | None:
        """Return the position of the guess marker, or ``None`` if none is placed."""
        return self.map.guess_coordinates

    def show_results(self, guess: Guess):
        """Show the round's result on the map and open the result overlay.
 
        Args:
            guess: The result of the current round.
        """
        self.map.show_guess_result(guess=guess)

        self.result_bar.place(in_=self.map, relx=0.5, y=10, anchor="n")
        self.result_bar.show(guess=guess)