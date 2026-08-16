"""Load the fixed inventory of places that make up the pool."""
from dataclasses import dataclass

import yaml

VIETNAM_LAT = (8.2, 23.4)
VIETNAM_LNG = (102.1, 109.5)
REGIONS = ("north", "central", "highlands", "south")


@dataclass(frozen=True)
class Place:
    id: str
    name: str
    region: str
    lat: float
    lng: float
    radius_km: int


def load_places(path: str) -> list[Place]:
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)

    places: list[Place] = []
    seen: set[str] = set()
    for entry in raw["places"]:
        place = Place(**entry)
        if place.id in seen:
            raise ValueError(f"duplicate place id: {place.id}")
        if place.region not in REGIONS:
            raise ValueError(f"{place.id}: unknown region {place.region}")
        seen.add(place.id)
        places.append(place)
    return places
