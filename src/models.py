from dataclasses import dataclass
from enum import Enum
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

    
    def padded(self, factor: float = 0.2) -> "BoundingBox":
        """create a margin for a bounding box by an amount of their own size"""
        lat_span = self.nw_corner.lat - self.se_corner.lat
        lon_span = self.se_corner.lon - self.nw_corner.lon

        lat_pad = lat_span * factor
        lon_pad = lon_span * factor

        return BoundingBox(
            nw_corner=Coordinates(
                lat=self.nw_corner.lat + lat_pad,
                lon=self.nw_corner.lon - lon_pad,
            ),
            se_corner=Coordinates(
                lat=self.se_corner.lat - lat_pad,
                lon=self.se_corner.lon + lon_pad,
            ),
        )

GERMANY_BOUNDING_BOX: BoundingBox = BoundingBox(
    nw_corner=Coordinates(lat=54.798054, lon=4.785561),
    se_corner=Coordinates(lat=47.630001, lon=15.373870))

EUROPE_BOUNDING_BOX: BoundingBox = BoundingBox(
    nw_corner=Coordinates(lat=58.301947, lon=-33.774550),
    se_corner=Coordinates(lat=36.146255, lon=34.053360))

# uses unintuitive coordinates because the map has a maximum zoom setting and can't display the whole map at once
WORLDWIDE_BOUNDING_BOX: BoundingBox = BoundingBox(
    nw_corner=Coordinates(lat=80, lon=-160),
    se_corner=Coordinates(lat=-10, lon=160))
class Difficulty(Enum):
    EASY = (
        0,
        90, 
        GERMANY_BOUNDING_BOX
    )
    STANDARD = (
        1,
        90, 
        GERMANY_BOUNDING_BOX
    )
    HARD = (
        2,
        550, 
        EUROPE_BOUNDING_BOX
    )
    EXTREME = (
        3,
        550, 
        EUROPE_BOUNDING_BOX
    )
    IMPOSSIBLE = (
        4,
        1492, 
        WORLDWIDE_BOUNDING_BOX
    )

    def __init__(self, id:int, decay_km: int, reset_bounding_box: BoundingBox):
        self.id = id # the id is required, so python can differentiate between each enum variant
        self.decay_km = decay_km # distance at which the score drops to 1/e of 5000 ≈ 1839
        self.reset_bounding_box = reset_bounding_box
