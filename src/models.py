from dataclasses import dataclass
from enum import Enum
from config import GERMANY_DIFFICULTY_COLOR, EUROPE_DIFFICULTY_COLOR, WORLDWIDE_DIFFICULTY_COLOR
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

@dataclass(frozen=True)
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
    
class Region(Enum):
    GERMANY = (
        GERMANY_DIFFICULTY_COLOR,
        BoundingBox(
            nw_corner=Coordinates(lat=54.798054, lon=4.785561),
            se_corner=Coordinates(lat=47.630001, lon=15.373870)),
        "Deutschland",
        None
    )
    EUROPE = ( 
        EUROPE_DIFFICULTY_COLOR,
        BoundingBox(
            nw_corner=Coordinates(lat=63.250020, lon=-14.884339),
            se_corner=Coordinates(lat=36.146255, lon=34.053360)),
        None,
        "Europa"
    )
    WORLDWIDE = (
        WORLDWIDE_DIFFICULTY_COLOR,
        # uses unintuitive coordinates because the map has a maximum zoom setting and can't display the whole map at once
        BoundingBox(
            nw_corner=Coordinates(lat=80, lon=-160),
            se_corner=Coordinates(lat=-10, lon=160)),
        None,
        None
    )

    def __init__(self, color: str, bounding_box: BoundingBox, country: str | None, continent: str | None) -> None:
        self.color = color
        self.bounding_box = bounding_box
        self.country = country
        self.continent = continent

@dataclass(frozen=True)
class DifficultySettings:
    id: int
    description: str
    region: Region
    min_population: int
    decay_km: int # distance at which the score drops to 1/e of 5000 ≈ 1839

class Difficulty(Enum):
    EASY = DifficultySettings(
            id=0,
            description="Only metropolises from inside Germany with more than 100.000 citizens",
            region=Region.GERMANY,
            min_population=100000,
            decay_km=150,
        )
    
    STANDARD = DifficultySettings(
            id = 1,
            description="Every German city with more than 50.000 citizens",
            region=Region.GERMANY,
            min_population=50000,
            decay_km=150,
        )
    
    HARD = DifficultySettings(
            id = 2,
            description="Cities in Europe with more than 200.000 citizens",
            region=Region.EUROPE,
            min_population=200000,
            decay_km=550,
        )
    EXTREME = DifficultySettings(
            id=3,
            description="European cities with more than 100.000 citizens",
            region=Region.EUROPE,
            min_population=100000,
            decay_km=550,
        )
    IMPOSSIBLE = DifficultySettings(
            id=4,
            description= "Every city in the world with more than 300.000 citizens",
            region=Region.WORLDWIDE,
            min_population= 300000,
            decay_km=1492,
        )

    def __init__(self, settings: DifficultySettings):
        self.settings: DifficultySettings = settings
