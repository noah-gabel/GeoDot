import customtkinter as ctk
from game_manager import Manager, GameState
from ui.game import GameScreen
from ui.start import MenuScreen
from ui.result import ResultScreen
from ui.screen import Screen
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

        self.menu_screen: Screen = MenuScreen(master=self, start_game=self._start_game)
        self.game_screen: Screen = GameScreen(master=self, round=self.round, current_city=self.current_city, current_score=self.current_score, guess_action=self._submit_guess)
        self.result_screen: Screen = ResultScreen(master=self)

        self.active_screen : Screen = self.menu_screen

    def _submit_guess(self):
        # checks wether the active screen is a GameScreen so that teh function will run
        # throws an error in case it is a wrong screen
        # this case should never occur when using the code correctly
        assert isinstance(self.active_screen, GameScreen), "wrong screen is being displayed"
        
        coordinates = self.active_screen.get_guess_coords()
        assert isinstance(coordinates, Coordinates), "no coordinates in the guess"

        game_state = self.game_manager.submit_guess(coordinates=coordinates)
        self._match_game_state_action(game_state=game_state)

    def _start_game(self, difficulty: Difficulty):
        game_state = self.game_manager.start_game(difficulty=difficulty)
        self._match_game_state_action(game_state=game_state)

    def _match_game_state_action(self, game_state: GameState):
        match game_state:
            case GameState.STARTING:
                self._switch_screen(screen=self.menu_screen)
            case GameState.GUESSING:
                self._update_to_game_screen()
            case GameState.SHOWING_RESULT:
                self._show_round_result()
            case GameState.FINISHED:
                self._switch_screen(screen=self.result_screen)

    def _update_to_game_screen(self):
        self._switch_screen(screen=self.game_screen)

        # assert wether the screen is a GameScreen instance in order for the linter to know
        # in reality it will always be a GameScreen
        assert isinstance(self.active_screen, GameScreen), "something went wrong during screen switch"

        # resetting the map and game screen for a new round
        self.active_screen.start_round(self.game_manager.difficulty)

        # update the StringVars for each round
        data = self.game_manager.get_game_screen_data()
        self.round.set(data.get("round", "N/A"))
        self.current_city.set(data.get("city_name", "N/A"))
        self.current_score.set(data.get("score", 0))

    def _show_round_result(self):
        assert isinstance(self.active_screen, GameScreen), "wrong screen is being displayed"
        self.active_screen.show_results(self.game_manager.get_current_guess())

        # call the helper function after 5 seconds so that you can use the returned GameState of the game manager
        self.after(5000, self._next_round_waiting)

    def _next_round_waiting(self):
        self._match_game_state_action(self.game_manager.next_round())

    def _switch_screen(self, screen : Screen):
        if self.active_screen is not screen:
            self.active_screen.hide()
            self.active_screen = screen
            self.active_screen.show()
    
    def start(self):
        self.active_screen.show()
        self.mainloop()
