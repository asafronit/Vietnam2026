"""Pipeline entry points: geocode, build, verify."""
import argparse
import glob
import os
import sys

import yaml

from .build import build_pool_kml
from .geocode import Geocoder, write_review_queue
from .inventory import load_places
from .schema import CATEGORIES, Record, validate_hotels, validate_record
from .verify import verify_kml, verify_within_radius

DATA_DIR = "data"
OUT_DIR = "out"
OUT_FILE = "vietnam-2026-pool.kml"
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


def cmd_build() -> int:
    places, records = _load_all()

    problems: list[str] = []
    for place in places:
        for rec in records[place.id]:
            problems.extend(validate_record(rec))
        hotels = [r for r in records[place.id] if r.category == "hotels"]
        problems.extend(validate_hotels(place.id, hotels))
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
    parser.add_argument("command", choices=["geocode", "build", "verify"])
    args = parser.parse_args(argv)
    return {"geocode": cmd_geocode, "build": cmd_build, "verify": cmd_verify}[
        args.command
    ]()


if __name__ == "__main__":
    raise SystemExit(main())
