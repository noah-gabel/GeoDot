from dataclasses import dataclass
from enum import Enum, auto
@dataclass(frozen=True)
class Coordinates:
    lat: float
    lon: float

@dataclass(frozen=True)
class City:
    name: str
    city_ONR: str
    coords: Coordinates

@dataclass(frozen=True)
class Guess:
    city: City
    coords: Coordinates
    distance: float
    score: int

class Difficulty(Enum):
    EASY = (
        0,
        90, 
        Coordinates(lat=50.708605, lon=10.287957), 
        7
    )
    STANDARD = (
        1,
        90, 
        Coordinates(lat=50.708605, lon=10.287957), 
        7
    )
    HARD = (
        2,
        550, 
        Coordinates(lat=47.721280, lon=11.604708), 
        5
    )
    EXTREME = (
        3,
        550, 
        Coordinates(lat=47.721280, lon=11.604708), 
        5
    )
    IMPOSSIBLE = (
        4,
        1492, 
        Coordinates(lat=47.721280, lon=11.604708), 
        4
    )

    def __init__(self, id:int, decay_km: int, reset_coordinates: Coordinates, reset_zoom: int):
        self.id = id # the id is required so that python can differentiate between each enum variant
        self.decay_km = decay_km
        self.reset_coordinates = reset_coordinates
        self.reset_zoom = reset_zoom

@dataclass
class BoundingBox:
    nw_corner: Coordinates
    se_corner : Coordinates

    # use @classmethod to construct a class object without having an existing instance of this class
    @classmethod
    def from_points(cls, points : list[Coordinates]) -> "BoundingBox":

        if len(points) < 1:
            raise ValueError("bounding box needs at least one point")
        
        latitudes = [point.lat for point in points]
        longitudes = [point.lon for point in points]

        south = min(latitudes)
        north = max(latitudes)
        west = min(longitudes)
        east = max(longitudes)
        
        return cls(
            nw_corner=Coordinates(north, west),
            se_corner=Coordinates(south, east)
        )


