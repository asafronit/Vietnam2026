"""Resolve place names to coordinates via OpenStreetMap Nominatim.

Free, no key. Nominatim's usage policy caps us at one request per second and
requires an identifying User-Agent. Results are cached to disk so a rerun
costs nothing.
"""
import json
import os
import time
from dataclasses import dataclass

import requests

from .inventory import Place
from .schema import Record
from .verify import LAT_RANGE, LNG_RANGE, haversine_km

ENDPOINT = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "vietnam2026-kml-pool/1.0 (personal trip planning)"
MIN_INTERVAL_SECONDS = 1.0


@dataclass
class GeocodeResult:
    lat: float | None
    lng: float | None
    accepted: bool
    reason: str


class Geocoder:
    def __init__(self, cache_path: str, session=None, sleep=time.sleep):
        self.cache_path = cache_path
        self.session = session or requests.Session()
        self.sleep = sleep
        self.cache: dict[str, list] = {}
        if os.path.exists(cache_path):
            with open(cache_path, encoding="utf-8") as fh:
                self.cache = json.load(fh)

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self.cache_path) or ".", exist_ok=True)
        with open(self.cache_path, "w", encoding="utf-8") as fh:
            json.dump(self.cache, fh, ensure_ascii=False, indent=1)

    def _lookup(self, query: str) -> list:
        if query in self.cache:
            return self.cache[query]
        self.sleep(MIN_INTERVAL_SECONDS)
        response = self.session.get(
            ENDPOINT,
            params={"q": query, "format": "json", "limit": 1, "countrycodes": "vn"},
            headers={"User-Agent": USER_AGENT},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        self.cache[query] = payload
        self._save()
        return payload

    def resolve(self, rec: Record, place: Place) -> GeocodeResult:
        hits = self._lookup(rec.geocode_query)
        if not hits:
            return GeocodeResult(None, None, False,
                                 f"no match for query {rec.geocode_query!r}")

        lat, lng = float(hits[0]["lat"]), float(hits[0]["lon"])

        if not (LAT_RANGE[0] <= lat <= LAT_RANGE[1]
                and LNG_RANGE[0] <= lng <= LNG_RANGE[1]):
            return GeocodeResult(lat, lng, False, f"{lat},{lng} is outside Vietnam")

        distance = haversine_km(place.lat, place.lng, lat, lng)
        if distance > place.radius_km:
            return GeocodeResult(
                lat, lng, False,
                f"{distance:.0f} km from {place.id} anchor, limit is "
                f"{place.radius_km} km",
            )

        return GeocodeResult(lat, lng, True, "ok")


def write_review_queue(
    path: str, rejected: list[tuple[str, Record, GeocodeResult]]
) -> None:
    lines = [
        "# Geocode review queue",
        "",
        "Entries below could not be placed with confidence. Fix the",
        "`geocode_query` in the place's YAML file, or set explicit `coords`,",
        "then rerun the geocode stage.",
        "",
        "| Place | Category | Name | Reason |",
        "|---|---|---|---|",
    ]
    for place_id, rec, result in rejected:
        lines.append(
            f"| {place_id} | {rec.category} | {rec.name} | {result.reason} |"
        )
    lines.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
