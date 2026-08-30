from dataclasses import dataclass
from enum import Enum, auto
@dataclass(frozen=True)
class Coordinates:
    lat: float
    lon: float

@dataclass(frozen=True)
class City():
    name: str
    city_ONR: str
    coords: Coordinates

@dataclass(frozen=True)
class Guess():
    city: City
    coords: Coordinates
    distance: float
    score: int

class Difficulty(Enum):
    EASY = (90)
    STANDARD = (90)
    HARD = (550)
    EXTREME = (550)
    IMPOSSIBLE = (1492)

    def __init__(self, decay_km):
        self.decay_km = decay_km


# may be unused in the future
@dataclass(frozen=True)
class BoundingBox:
    south_west_corner: Coordinates
    north_east_corner: Coordinates