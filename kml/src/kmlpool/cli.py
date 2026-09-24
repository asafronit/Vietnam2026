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
from .schema import (
    CATEGORIES,
    Record,
    WEATHER_SENSITIVITY,
    is_shippable,
    is_web_shippable,
    validate_hebrew,
    validate_hotels,
    validate_record,
)
from .style import PLACE_COLORS
from .verify import verify_kml, verify_within_radius

DATA_DIR = "data"
OUT_DIR = "out"
OUT_FILE = "vietnam-2026-pool.kml"
WEB_OUT_FILE = "poi-data.js"
CACHE = "cache/nominatim.json"


# Top-level YAML keys that are place metadata rather than a category of
# records. Both the loader and `_persist` walk `raw.items()` assuming every
# value is a list of entries, so a scalar key here would raise in the loader
# and iterate a bool in `_persist`. Keep this the single list both consult.
NON_CATEGORY_KEYS = ("hebrew_complete",)


def load_hebrew_flag(path: str) -> bool:
    """Whether this place declares its Hebrew content finished."""
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    return bool(raw.get("hebrew_complete", False))


def load_records(path: str) -> list[Record]:
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}

    records: list[Record] = []
    for key, entries in raw.items():
        if key in NON_CATEGORY_KEYS:
            continue
        if key not in CATEGORIES:
            raise ValueError(f"{path}: unknown category {key!r}")
        for entry in entries or []:
            entry = dict(entry)
            entry.pop("dish", None)  # informational only
            coords = entry.pop("coords", None)  # written back by cmd_geocode
            if coords is not None:
                entry["lat"] = coords["lat"]
                entry["lng"] = coords["lng"]
            rec = Record(category=key, **entry)
            # Hotel prices predate price_unit and are all per night. Filling
            # the default here keeps the YAML free of a line that only ever
            # says the same thing.
            if rec.category == "hotels" and rec.price_low is not None and rec.price_unit is None:
                rec.price_unit = "per_night"
            records.append(rec)
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
            # A dish has no address. Sending it to the geocoder produces either
            # a miss or a pin on a city centre it has no connection to, and
            # either way it lands in the review queue as unfixable noise.
            if rec.is_dish:
                continue
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
        if category in NON_CATEGORY_KEYS:
            continue
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
        problems.extend(
            validate_hebrew(
                place.id,
                records[place.id],
                load_hebrew_flag(os.path.join(DATA_DIR, f"{place.id}.yaml")),
            )
        )
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
    # Hebrew twins ship only when they exist; the page falls back to English.
    for src, key in (
        (rec.name_he, "nameHe"),
        (rec.area_he, "areaHe"),
        (rec.what_he, "whatHe"),
        (rec.why_he, "whyHe"),
    ):
        if src:
            data[key] = src
    data["priceUnit"] = rec.price_unit
    if rec.tier_official is not None:
        data["tierOfficial"] = rec.tier_official
    data["priceLow"] = rec.price_low
    data["priceHigh"] = rec.price_high
    if rec.price_checked is not None:
        data["priceChecked"] = rec.price_checked
    data["avoid"] = rec.avoid
    data["kind"] = rec.kind
    data["isDish"] = rec.is_dish
    data["signal"] = rec.signal
    data["video"] = rec.video
    # Contact routes ship only when present. The page renders whatsapp as the
    # purple action the link convention reserves for reaching a person; the
    # other two are plain tel: and mailto: links.
    for src, key in ((rec.whatsapp, "whatsapp"), (rec.phone, "phone"), (rec.email, "email")):
        if src:
            data[key] = src
    # Weather sensitivity travels with the record so the page never has to
    # guess it. The per-record override wins; otherwise the category default.
    data["weather"] = rec.weather or WEATHER_SENSITIVITY.get(rec.category, "medium")
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
            # The web pool ships records the KML cannot: a card without
            # coordinates still carries its name, description and reason,
            # and links out to a maps search instead of a pin.
            if not is_web_shippable(rec):
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


def cmd_hebrew_report() -> int:
    """Per-place Hebrew coverage. The progress map for the translation work.

    Counts only records the web pool would actually ship, because a record the
    site never renders is not a gap a reader can see.
    """
    places, records = _load_all()

    rows = []
    for place in places:
        shippable = [r for r in records[place.id] if is_web_shippable(r)]
        done = [
            r for r in shippable
            if (r.what_he or "").strip() and (r.why_he or "").strip()
        ]
        declared = load_hebrew_flag(os.path.join(DATA_DIR, f"{place.id}.yaml"))
        rows.append((place.id, len(done), len(shippable), declared))

    width = max(len(r[0]) for r in rows)
    print(f"{'place'.ljust(width)}  translated  total   pct  declared")
    for pid, done, total, declared in rows:
        pct = (100 * done // total) if total else 0
        flag = "yes" if declared else "-"
        print(f"{pid.ljust(width)}  {done:>10}  {total:>5}  {pct:>3}%  {flag}")

    total_done = sum(r[1] for r in rows)
    total_all = sum(r[2] for r in rows)
    pct = (100 * total_done // total_all) if total_all else 0
    complete = sum(1 for r in rows if r[3])
    print(f"{'TOTAL'.ljust(width)}  {total_done:>10}  {total_all:>5}  {pct:>3}%  "
          f"{complete}/{len(rows)} places declared complete")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kmlpool")
    parser.add_argument(
        "command",
        choices=["geocode", "build", "verify", "web", "hebrew-report"],
    )
    args = parser.parse_args(argv)
    return {
        "geocode": cmd_geocode,
        "build": cmd_build,
        "verify": cmd_verify,
        "web": cmd_web,
        "hebrew-report": cmd_hebrew_report,
    }[args.command]()


if __name__ == "__main__":
    raise SystemExit(main())
