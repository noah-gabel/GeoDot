from dataclasses import dataclass

@dataclass(frozen=True)
class City():
    name: str
    city_ONR: str
    latitude: float     #breite
    longitude: float    #länge
