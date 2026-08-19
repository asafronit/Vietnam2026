"""Pipeline entry points: geocode, build, verify, web."""
import argparse
import glob
import json
import os
import sys

import yaml

from .build import build_place_kml, build_pool_kml
from .geocode import Geocoder, write_review_queue
from .inventory import load_places
from .schema import CATEGORIES, Record, is_shippable, validate_hotels, validate_record
from .style import PLACE_COLORS
from .verify import verify_kml, verify_within_radius

DATA_DIR = "data"
OUT_DIR = "out"
OUT_FILE = "vietnam-2026-pool.kml"
WEB_OUT_FILE = "poi-data.js"
CACHE = "cache/nominatim.json"


def load_records(path: str) -> list[Record]:
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}

    records: list[Record] = []
    for key, entries in raw.items():
        if key not in CATEGORIES:
            raise ValueError(f"{path}: unknown category {key!r}")
        for entry in entries or []:
            entry = dict(entry)
            entry.pop("dish", None)  # informational only
            coords = entry.pop("coords", None)  # written back by cmd_geocode
            if coords is not None:
                entry["lat"] = coords["lat"]
                entry["lng"] = coords["lng"]
            records.append(Record(category=key, **entry))
    return records


def _load_all() -> tuple[list, dict[str, list[Record]]]:
    places = load_places(os.path.join(DATA_DIR, "places.yaml"))
    records: dict[str, list[Record]] = {}
    for place in places:
        path = os.path.join(DATA_DIR, f"{place.id}.yaml")
        records[place.id] = load_records(path) if os.path.exists(path) else []
    return places, records


def cmd_geocode() -> int:
    places, records = _load_all()
    geo = Geocoder(CACHE)
    rejected = []
    for place in places:
        for rec in records[place.id]:
            result = geo.resolve(rec, place)
            if result.accepted:
                rec.lat, rec.lng = result.lat, result.lng
                rec.location_precision = (
                    "approximate" if result.precision == "approximate" else None
                )
            else:
                rejected.append((place.id, rec, result))
        _persist(place.id, records[place.id])

    write_review_queue("review-queue.md", rejected)
    print(f"geocoded, {len(rejected)} rejected -> review-queue.md")
    return 0


def _persist(place_id: str, records: list[Record]) -> None:
    """Write resolved coordinates back into the place's YAML."""
    path = os.path.join(DATA_DIR, f"{place_id}.yaml")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    by_name = {(r.category, r.name): r for r in records}
    for category, entries in raw.items():
        for entry in entries or []:
            rec = by_name.get((category, entry["name"]))
            if rec and rec.lat is not None:
                entry["coords"] = {"lat": rec.lat, "lng": rec.lng}
                if rec.location_precision == "approximate":
                    entry["location_precision"] = "approximate"
                else:
                    entry.pop("location_precision", None)
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(raw, fh, allow_unicode=True, sort_keys=False)


def _validate_all(places: list, records: dict[str, list[Record]]) -> list[str]:
    """Every record/hotel-tier check cmd_build and cmd_web both gate on
    before writing anything. Shared so the two outputs can't silently drift
    apart on what counts as valid."""
    problems: list[str] = []
    for place in places:
        for rec in records[place.id]:
            problems.extend(validate_record(rec))
        hotels = [r for r in records[place.id] if r.category == "hotels"]
        problems.extend(validate_hotels(place.id, hotels))
    return problems


def cmd_build() -> int:
    places, records = _load_all()

    problems = _validate_all(places, records)
    if problems:
        for p in problems:
            print(f"INVALID: {p}", file=sys.stderr)
        return 1

    os.makedirs(OUT_DIR, exist_ok=True)
    target = os.path.join(OUT_DIR, OUT_FILE)
    with open(target, "wb") as fh:
        fh.write(build_pool_kml(places, records))

    shipped = sum(1 for rs in records.values() for r in rs if r.lat is not None)
    print(f"built {target} ({shipped} pins across 7 layers)")

    # One file per station, alongside the pool file. Numbered by the order
    # in places.yaml so filenames sort in itinerary order.
    for index, place in enumerate(places, start=1):
        place_records = records.get(place.id, [])
        station_file = f"{index:02d}-{place.id}.kml"
        station_path = os.path.join(OUT_DIR, station_file)
        with open(station_path, "wb") as fh:
            fh.write(build_place_kml(place, place_records))
        station_shipped = sum(1 for r in place_records if r.lat is not None)
        print(f"built {station_path} ({station_shipped} pins)")

    return 0


def _record_to_web_json(rec: Record) -> dict:
    """Map a shippable Record onto the camelCase shape design_1_map.html
    expects. Field names are chosen explicitly, not derived from the
    dataclass, so a future Record field never leaks into the page by
    accident.

    `tier`, `priceLow`, `priceHigh`, `avoid`, `kind`, `signal` and `video`
    are always emitted (as null when unset) so the page never has to test
    for key existence. Every other optional key (`tierOfficial`,
    `priceChecked`) is omitted entirely when unset.
    """
    data: dict = {
        "name": rec.name,
        "area": rec.area,
        "what": rec.what,
        "why": rec.why,
        "lat": rec.lat,
        "lng": rec.lng,
        "approx": rec.location_precision == "approximate",
        "sources": rec.sources,
        "tier": rec.tier,
    }
    if rec.tier_official is not None:
        data["tierOfficial"] = rec.tier_official
    data["priceLow"] = rec.price_low
    data["priceHigh"] = rec.price_high
    if rec.price_checked is not None:
        data["priceChecked"] = rec.price_checked
    data["avoid"] = rec.avoid
    data["kind"] = rec.kind
    data["signal"] = rec.signal
    data["video"] = rec.video
    return data


def cmd_web() -> int:
    places, records = _load_all()

    problems = _validate_all(places, records)
    if problems:
        for p in problems:
            print(f"INVALID: {p}", file=sys.stderr)
        return 1

    data: dict = {}
    for index, place in enumerate(places, start=1):
        poi: dict[str, list] = {category: [] for category in CATEGORIES}
        for rec in records.get(place.id, []):
            if not is_shippable(rec):
                continue
            poi[rec.category].append(_record_to_web_json(rec))
        counts = {category: len(poi[category]) for category in CATEGORIES}
        data[place.id] = {
            "id": place.id,
            "name": place.name,
            "region": place.region,
            "seq": index,
            "lat": place.lat,
            "lng": place.lng,
            "color": PLACE_COLORS[place.id],
            "counts": counts,
            "poi": poi,
        }

    os.makedirs(OUT_DIR, exist_ok=True)
    target = os.path.join(OUT_DIR, WEB_OUT_FILE)
    payload = json.dumps(data, indent=2, ensure_ascii=False)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(f"const POI_DATA = {payload};\n")

    total = sum(len(recs) for place_data in data.values() for recs in place_data["poi"].values())
    print(f"built {target} ({total} records across {len(places)} places)")
    return 0


def cmd_verify() -> int:
    places, records = _load_all()
    errors = verify_within_radius(places, records)
    for path in sorted(glob.glob(os.path.join(OUT_DIR, "*.kml"))):
        with open(path, "rb") as fh:
            errors.extend(f"{os.path.basename(path)}: {e}"
                          for e in verify_kml(fh.read()))
    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print("all checks passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kmlpool")
    parser.add_argument("command", choices=["geocode", "build", "verify", "web"])
    args = parser.parse_args(argv)
    return {
        "geocode": cmd_geocode,
        "build": cmd_build,
        "verify": cmd_verify,
        "web": cmd_web,
    }[args.command]()


if __name__ == "__main__":
    raise SystemExit(main())
