import math
from models import Coordinates, Difficulty
from config import EARTH_RADIUS, GUESS_TOLERANCE_KM

# calculate the score from the distance between the points
# the points go down exponentially and depending on the mode you play
def calculate_score(
        distance_km: float,
        difficulty: Difficulty):
    
    # use max(distance -tolerance, 0) so that the function can never output anything beyond 5000 points
    score = 5000 * math.exp(-(max(distance_km - GUESS_TOLERANCE_KM, 0)) / difficulty.decay_km)
    
    return round(score)
    


# calculates the distance between two coordinates with the haversine algorithm
def haversine_distance(guess_coordinates : Coordinates , city_coordinates : Coordinates) -> float:
    # calculate the Radian values
    phi1 = math.radians(guess_coordinates.lat)
    phi2 = math.radians(city_coordinates.lat)
    delta_phi = math.radians(city_coordinates.lat - guess_coordinates.lat)      # delta breite
    delta_lambda = math.radians(city_coordinates.lon - guess_coordinates.lon)   # delta länge

    # Haversine formula
    # value between 0 and 1
    # describes the distance measured through the earth
    # 0 = both points are at the same position
    # 1 = both points are exactly at the opposite sides of the earth
    length = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )

    # angle form the earth's center
    angle = 2 * math.atan2(math.sqrt(length), math.sqrt(1 - length))

    distance = EARTH_RADIUS * angle

    return round(distance, 2)

