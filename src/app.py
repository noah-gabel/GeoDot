import customtkinter as ctk
from game_manager import Manager, GameState
from ui.game import GameScreen
from ui.start import MenuScreen
from ui.result import ResultScreen
from ui.screen import Screen
from config import FG_COLOR, ICON_DIR
from models import Coordinates, Difficulty

class App(ctk.CTk):

    def __init__(self, game_manager: Manager, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color=FG_COLOR)
        self.game_manager = game_manager
        self.title("GeoDot")

        # change the window to fullscreen
        # delay is needed in order for it to work
        self.after(1, lambda: self.state("zoomed"))

        self._set_icon()

        self.current_city = ctk.StringVar(value="N/A")
        self.round = ctk.StringVar(value="N/A")
        self.current_score = ctk.IntVar(value=0)

        # setup screens once at startup to avoid rebuilding tiles every time teh screen switches
        self.menu_screen: MenuScreen = MenuScreen(master=self, start_game=self._start_game)
        self.game_screen: GameScreen = GameScreen(master=self, rounds=self.round, current_city=self.current_city, current_score=self.current_score, guess_action=self._submit_guess, next_round=self._next_round_waiting)
        self.result_screen: ResultScreen = ResultScreen(master=self, total_score=self.current_score, play_again=self._play_again, change_difficulty=self.reset)

        self.active_screen : Screen = self.menu_screen

    def _set_icon(self):
        self.iconbitmap(f"{ICON_DIR}/geodot.ico")

    def reset(self):
        self.menu_screen.reset()
        self.result_screen.reset(self.game_manager.difficulty)
        self._match_game_state_action(self.game_manager.reset())

    def _submit_guess(self):
        # checks whether the active screen is a GameScreen so that the function will run
        # throws an error in case it is a wrong screen
        # this case should never occur when using the code correctly
        assert isinstance(self.active_screen, GameScreen), "wrong screen is being displayed"
        
        coordinates = self.active_screen.get_guess_coords()
        if isinstance(coordinates, Coordinates):
            game_state = self.game_manager.submit_guess(coordinates=coordinates)
            self._match_game_state_action(game_state=game_state)
        else:
            raise RuntimeError("no coordinates in the guess")

    def _play_again(self):
        self._start_game(difficulty=self.game_manager.difficulty)

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
                assert isinstance(self.active_screen, ResultScreen), "Switching screens didn't work. Can only access the reset function on a ResultScreen"
                self.active_screen.reset(self.game_manager.difficulty)
                self.active_screen.show_results(results=self.game_manager.results, difficulty=self.game_manager.difficulty)

    def _update_to_game_screen(self):
        self._switch_screen(screen=self.game_screen)

        # assert whether the screen is a GameScreen instance in order for the linter to know
        # in reality it will always be a GameScreen
        assert isinstance(self.active_screen, GameScreen), "something went wrong during screen switch"

        # resetting the map and game screen for a new round
        self.active_screen.start_round(self.game_manager.difficulty)

        # update the StringVars for each round
        # necessary at this step for the first round
        data = self.game_manager.get_game_screen_data()
        self.round.set(data.get("round", "N/A"))
        self.current_city.set(data.get("city_name", "N/A"))
        self.current_score.set(data.get("score", 0))

    def _show_round_result(self):
        assert isinstance(self.active_screen, GameScreen), "wrong screen is being displayed"
        self.active_screen.show_results(self.game_manager.get_current_guess())

        # update the StringVars for each round
        # necessary at this step for the last round and instant feedback while seeing the result
        data = self.game_manager.get_game_screen_data()
        self.round.set(data.get("round", "N/A"))
        self.current_city.set(data.get("city_name", "N/A"))
        self.current_score.set(data.get("score", 0))

    def _next_round_waiting(self):
        """ callback function for the countdown to start the next round
            needs to be a separate function in order for the returned game_state to be captured and evaluated
        """
        self._match_game_state_action(self.game_manager.next_round())

    def _switch_screen(self, screen : Screen):
        if self.active_screen is not screen:
            self.active_screen.hide()
            self.active_screen = screen
            self.active_screen.show()
    
    def start(self):
        self.active_screen.show()
        self.mainloop()
