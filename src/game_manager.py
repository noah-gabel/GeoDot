"""Game logic independent of the user interface."""

from enum import Enum, auto

from database import Database
from models import City, Coordinates, Difficulty, Guess
from score import calculate_score, haversine_distance


class GameState(Enum):
    """Phases of a game.

    ``Manager`` methods return the new state so the UI can decide which screen to show next.
    """

    STARTING = auto()  # idle screen with difficulties and start button
    GUESSING = auto()  # playing and looking for a guess
    SHOWING_RESULT = (
        auto()
    )  # showing the results of the current round and starting the next one
    FINISHED = auto()  # show end results and give the ability to play again


class Manager:
    """Runs the complete game logic.

    The manager is a small state machine. Methods which advance the game, return a new ``GameState``. It has no knowledge of the UI.

    Args:
        database: Instance of ``Database``. Source of the cities for each game.
    """

    def __init__(self, database: Database):
        self.database = database
        self.game_state = GameState.STARTING

    def start_game(self, difficulty: Difficulty) -> GameState:
        """Start a new game and load its cities.

        Resets the score, round counter and results. Due to that fact, this method can be used as a play again feature

        Args:
            difficulty: Decides which cities are loaded and how guesses are scored.

        Returns:
            ``GameState.GUESSING``.
        """
        self.difficulty = difficulty
        self.total_score: int = 0
        self.current_round_index: int = 0
        self.results: list[Guess] = []

        city_data = self.database.get_random_cities(difficulty)
        self.cities: list[City] = [
            City(
                city_ONR=city_ONR,
                name=name,
                coords=Coordinates(lat=latitude, lon=longitude),
            )
            for (city_ONR, name, latitude, longitude) in city_data
        ]

        self.game_state = GameState.GUESSING
        return self.game_state

    def submit_guess(self, coordinates: Coordinates) -> GameState:
        """Score the player's guess for the current round.

        Args:
            coordinates: Where the player placed their marker.

        Returns:
            ``GameState.SHOWING_RESULT``.

        Raises:
            RuntimeError: If the game is not in ``GameState.GUESSING``.
        """
        if self.game_state != GameState.GUESSING:
            raise RuntimeError(
                "can't submit a guess unless the game is in guessing mode"
            )

        distance = haversine_distance(
            guess_coordinates=coordinates,
            city_coordinates=self.cities[self.current_round_index].coords,
        )

        self.round_score = calculate_score(
            distance_km=distance, difficulty=self.difficulty
        )
        self.total_score += self.round_score

        guess = Guess(
            city=self.cities[self.current_round_index],
            coords=coordinates,
            distance=distance,
            score=self.round_score,
        )
        self.results.append(guess)

        self.game_state = GameState.SHOWING_RESULT
        return self.game_state

    def next_round(self) -> GameState:
        """Skip to the next round, or finish the game after the last one.

        Returns:
            ``GameState.GUESSING`` if another round follows, otherwise ``GameState.FINISHED``.

        Raises:
            RuntimeError: If the game is not in ``GameState.SHOWING_RESULT``.
        """
        if self.game_state != GameState.SHOWING_RESULT:
            raise RuntimeError(
                "can't go to the next round unless you are in teh SHOW_RESULT state"
            )

        if self.current_round_index >= len(self.cities) - 1:
            self.game_state = GameState.FINISHED
            return self.game_state

        self.current_round_index += 1
        self.game_state = GameState.GUESSING
        return self.game_state

    def get_game_screen_data(self) -> dict:
        """Return the values shown in the in game HUD.

        Returns:
            A dict with ``city_name`` (the city to find), ``round`` (e.g. ``"3/10"``) and ``score`` (total score so far).
        """
        return {
            "city_name": self.cities[self.current_round_index].name,
            "round": f"{self.current_round_index + 1}/{len(self.cities)}",
            "score": self.total_score,
        }

    def reset(self) -> GameState:
        """Return to the difficulty selection.

        The results of the last game stay available until the next ``start_game`` call.

        Returns:
            ``GameState.STARTING``.
        """
        self.game_state = GameState.STARTING
        return self.game_state

    def get_current_guess(self) -> Guess:
        """Return the guess submitted in the current round.

        Raises:
            ValueError: If no guess has been submitted yet.
        """
        if self.current_round_index < 0 or len(self.results) < 1:
            raise ValueError(
                "you should only call this function after submitting a guess"
            )

        return self.results[self.current_round_index]
