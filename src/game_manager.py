from database import Database
from enum import Enum, auto
from models import City, Guess, Coordinates, Difficulty
from score import haversine_distance, calculate_score

class GameState(Enum):
    STARTING = auto()       #idle screen with difficulties and start button
    GUESSING = auto()       #playing and looking for a guess
    SHOWING_RESULT = auto() #showing the results of the current round and starting the next one
    FINISHED = auto()       #show end results and give the ability to play again


class Manager():
    def __init__(self, database: Database):
        self.database = database
        self.game_state = GameState.STARTING

    def start_game(self, difficulty : Difficulty) -> GameState:
        try:
            self.difficulty = difficulty
            self.total_score: int = 0

            # TODO remove the amount only for testing
            city_data = self.database.get_random_cities(difficulty, amount=1)
            self.cities: list[City] = [City(city_ONR=city_ONR,name=name, coords=Coordinates(lat=latitude, lon=longitude)) for (city_ONR, name, latitude, longitude) in city_data]

            self.results: list[Guess] = []

            self.current_round_index : int = 0
            self.game_state = GameState.GUESSING
        
        except Exception as e:
            #TODO add a logger or at least print/show a valuable error message
            print(f"Error occurred: {e}")

        return self.game_state


    def submit_guess(self, coordinates: Coordinates) -> GameState:
        distance = haversine_distance(
            guess_coordinates=coordinates, 
            city_coordinates=self.cities[self.current_round_index].coords
        )

        self.round_score = calculate_score(distance_km=distance, difficulty=self.difficulty)
        self.total_score += self.round_score

        guess = Guess(
            city=self.cities[self.current_round_index], 
            coords=coordinates, 
            distance=distance, 
            score=self.round_score
        )
        self.results.append(guess)
        
        self.game_state = GameState.SHOWING_RESULT
        return self.game_state

    def next_round(self) -> GameState:
        if self.current_round_index >= len(self.cities) -1:
            self.game_state = GameState.FINISHED
            return self.game_state

        self.current_round_index += 1
        self.game_state = GameState.GUESSING
        return self.game_state
        
    def get_game_screen_data(self) -> dict:
        return {
            "city_name": self.cities[self.current_round_index].name,
            "round": f"{self.current_round_index + 1}/{len(self.cities)}",
            "score": self.total_score
        }

    def get_current_guess(self) -> Guess:
        if self.current_round_index < 0 or len(self.results) < 1:
            raise ValueError("you should only call this function after submitting a guess")

        return self.results[self.current_round_index]
