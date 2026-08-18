"""Resolve place names to coordinates via OpenStreetMap Nominatim.

Free, no key. Nominatim's usage policy caps us at one request per second and
requires an identifying User-Agent. Results are cached to disk so a rerun
costs nothing.
"""
import json
import os
import re
import time
from dataclasses import dataclass

import requests

from .inventory import Place
from .schema import Record
from .verify import LAT_RANGE, LNG_RANGE, haversine_km

ENDPOINT = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "vietnam2026-kml-pool/1.0 (personal trip planning)"
MIN_INTERVAL_SECONDS = 1.0

# Fallback-ladder query construction. Over-specifying (district name plus a
# local-name alias) reliably defeats Nominatim's free-text search; these
# rungs progressively coarsen the query. See Task 7b diagnosis.
_PARENTHETICAL_RE = re.compile(r"\s*\([^)]*\)")
_BASE_SEPARATORS = (" and ", " - ", " – ")  # hyphen and en dash
_CITY_SEPARATORS = (" and ",)


def _truncate_at_first(text: str, separators: tuple[str, ...]) -> str:
    cut = len(text)
    for sep in separators:
        idx = text.find(sep)
        if idx != -1 and idx < cut:
            cut = idx
    return text[:cut].strip()


def _base_name(name: str) -> str:
    """`name` with any parenthetical removed and truncated at the first
    ' and ', ' - ' or ' – '. Feeds the two coarsest fallback rungs."""
    stripped = _PARENTHETICAL_RE.sub("", name)
    stripped = re.sub(r"\s+", " ", stripped).strip()
    return _truncate_at_first(stripped, _BASE_SEPARATORS)


def _city_name(place_name: str) -> str:
    """Compound place names ("Hoi An and Da Nang") truncated to their first
    component for use in a fallback query."""
    return _truncate_at_first(place_name, _CITY_SEPARATORS)


@dataclass
class GeocodeResult:
    lat: float | None
    lng: float | None
    accepted: bool
    reason: str
    # "exact" for a rung-1 hit (the record's geocode_query as written),
    # "approximate" for anything recovered by a fallback rung.
    precision: str = "exact"


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
        """Try the query ladder in order, stopping at the first rung that
        both returns a hit and passes the confidence gate (Vietnam bounding
        box, then the place's radius). Rung 1 is the record's geocode_query
        exactly as written -- unchanged from the pre-ladder behaviour, and
        the only rung that counts as "exact"; rungs 2-4 are progressively
        coarser fallbacks and are marked "approximate" when they succeed.
        """
        city = _city_name(place.name)
        base = _base_name(rec.name)
        rungs = [
            (rec.geocode_query, "exact"),
            (f"{rec.name}, {city}, Vietnam", "approximate"),
            (f"{base}, {city}, Vietnam", "approximate"),
            (f"{base}, Vietnam", "approximate"),
        ]

        last_result: GeocodeResult
        for query, precision in rungs:
            hits = self._lookup(query)
            if not hits:
                last_result = GeocodeResult(
                    None, None, False, f"no match for query {query!r}", precision
                )
                continue

            lat, lng = float(hits[0]["lat"]), float(hits[0]["lon"])

            if not (LAT_RANGE[0] <= lat <= LAT_RANGE[1]
                    and LNG_RANGE[0] <= lng <= LNG_RANGE[1]):
                last_result = GeocodeResult(
                    lat, lng, False, f"{lat},{lng} is outside Vietnam", precision
                )
                continue

            distance = haversine_km(place.lat, place.lng, lat, lng)
            if distance > place.radius_km:
                last_result = GeocodeResult(
                    lat, lng, False,
                    f"{distance:.0f} km from {place.id} anchor, limit is "
                    f"{place.radius_km} km",
                    precision,
                )
                continue

            return GeocodeResult(lat, lng, True, "ok", precision)

        return last_result


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
