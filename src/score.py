import math

from config import EARTH_RADIUS, GUESS_TOLERANCE_KM, MAX_ROUND_SCORE
from models import Coordinates, Difficulty


def calculate_score(distance_km: float, difficulty: Difficulty):
    """Convert the distance of a guess into points.

    Guesses within ``GUESS_TOLERANCE_KM`` earn the full ``MAX_ROUND_SCORE``.
    Beyond that, the score decays exponentially at a rate set by the
    difficulty's ``decay_km``.

    Args:
        distance_km: Distance between the guess and the city in kilometers.
        difficulty: Difficulty whose ``decay_km`` controls the falloff.

    Returns:
        Points for the round, from 0 up to ``MAX_ROUND_SCORE``.
    """
    # max(..., 0) keeps the exponent at or below zero, so the score never exceeds MAX_ROUND_SCORE
    score = MAX_ROUND_SCORE * math.exp(
        -(max(distance_km - GUESS_TOLERANCE_KM, 0)) / difficulty.settings.decay_km
    )

    return round(score)


def haversine_distance(
    guess_coordinates: Coordinates, city_coordinates: Coordinates
) -> float:
    """Return the great-circle distance between two points on Earth.

    Uses the haversine formula on a sphere with radius ``EARTH_RADIUS``

    Args:
        guess_coordinates: Where the player placed their marker.
        city_coordinates: Actual location of the city.

    Returns:
        Distance in kilometers, rounded to two decimal places.
    """

    phi1 = math.radians(guess_coordinates.lat)
    phi2 = math.radians(city_coordinates.lat)
    delta_phi = math.radians(
        city_coordinates.lat - guess_coordinates.lat
    )  # delta breite
    delta_lambda = math.radians(
        city_coordinates.lon - guess_coordinates.lon
    )  # delta länge

    # Haversine formula
    # value between 0 and 1
    # describes the distance measured through the earth
    # 0 = both points are at the same position
    # 1 = both points are exactly at the opposite sides of the earth
    length = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )

    # angle between the two points, seen from the earth's center
    angle = 2 * math.atan2(math.sqrt(length), math.sqrt(1 - length))

    distance = EARTH_RADIUS * angle

    return round(distance, 2)
