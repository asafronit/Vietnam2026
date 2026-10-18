import kmlpool.cli as cli_module
import yaml

from kmlpool.cli import _persist, load_records
from kmlpool.schema import Record


FIXTURE = """
hotels:
- name: Example Hotel
  tier: 5
  tier_official: true
  price_low: 80
  price_high: 137
  price_checked: '2026-08-16'
  area: Old Quarter
  what: A hotel used only as a loader fixture.
  why: Pins the loader behaviour, not the research content
  confidence: high
  geocode_query: Example Hotel, Hanoi, Vietnam
  sources:
  - https://example.test/a
  - https://example.test/b
must_see:
- name: Example Lake
  area: Old Quarter
  what: A lake used only as a loader fixture.
  why: Pins the loader behaviour, not the research content
  confidence: high
  geocode_query: Example Lake, Hanoi, Vietnam
  sources:
  - https://example.test/c
food:
- name: Example Noodles
  kind: vietnamese
  signal: traveler_recommended
  dish: Bun cha
  area: Hai Ba Trung
  what: A noodle shop used only as a loader fixture.
  why: Pins the loader behaviour, not the research content
  confidence: high
  geocode_query: Example Noodles, Hanoi, Vietnam
  sources:
  - https://example.test/d
"""


def _fixture(tmp_path):
    """A fixture of our own.

    These tests assert how `load_records` behaves, not what the research
    happens to contain. Reading data/hanoi.yaml coupled them to a file the
    research task legitimately rewrites, so they broke the moment real data
    landed. Own the input instead.
    """
    path = tmp_path / "place.yaml"
    path.write_text(FIXTURE, encoding="utf-8")
    return str(path)


def test_loads_records_across_categories(tmp_path):
    records = load_records(_fixture(tmp_path))
    categories = {r.category for r in records}
    assert categories == {"hotels", "must_see", "food"}


def test_category_is_taken_from_the_yaml_key(tmp_path):
    records = load_records(_fixture(tmp_path))
    hotel = next(r for r in records if r.name == "Example Hotel")
    assert hotel.category == "hotels"
    assert hotel.tier == 5


def test_dish_is_dropped_rather_than_passed_to_record(tmp_path):
    """`dish` is informational only; Record has no such field."""
    records = load_records(_fixture(tmp_path))
    noodles = next(r for r in records if r.name == "Example Noodles")
    assert not hasattr(noodles, "dish")
    assert noodles.signal == "traveler_recommended"


def test_records_start_ungeocoded(tmp_path):
    # Deliberately not data/hanoi.yaml: `geocode` persists resolved `coords`
    # back into that exact file (that's the round-trip this module exists to
    # get right), so once the live pipeline has run once, hanoi.yaml is no
    # longer ungeocoded. A unit test asserting "no coords yet" needs its own
    # fixture that nothing else mutates.
    fixture = tmp_path / "ungeocoded.yaml"
    fixture.write_text(
        "must_see:\n"
        "  - name: Test Place\n"
        "    area: Test Area\n"
        "    what: A place with no coordinates recorded yet.\n"
        "    why: Confirms load_records leaves lat and lng unset by default.\n"
        "    confidence: high\n"
        "    geocode_query: Test Place, Hanoi, Vietnam\n",
        encoding="utf-8",
    )
    assert all(r.lat is None for r in load_records(str(fixture)))


def test_unknown_yaml_key_raises(tmp_path):
    import pytest
    bad = tmp_path / "bad.yaml"
    bad.write_text("nightclubs:\n  - name: X\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unknown category"):
        load_records(str(bad))


def test_coords_written_by_geocode_are_read_back(tmp_path):
    """Pins the bug: cmd_geocode's _persist writes a `coords: {lat, lng}`
    key back into the YAML, but Record has no `coords` field, only `lat`
    and `lng`. load_records must pop `coords` and hydrate lat/lng from it
    so a second geocode -> build run doesn't crash or ship an empty map.
    """
    fixture = tmp_path / "coords.yaml"
    fixture.write_text(
        """
must_see:
  - name: Test Place
    area: Test Area
    what: A test place used only to verify the coords round-trip.
    why: Confirms geocode-written coordinates survive a reload intact.
    confidence: high
    geocode_query: Test Place, Hanoi, Vietnam
    coords:
      lat: 21.03
      lng: 105.85
""",
        encoding="utf-8",
    )
    records = load_records(str(fixture))
    assert len(records) == 1
    assert records[0].lat == 21.03
    assert records[0].lng == 105.85


def test_location_precision_written_by_geocode_is_read_back(tmp_path):
    """The fallback ladder (Task 7b) marks fallback hits `approximate` so
    the map can render a visible caveat. load_records must round-trip it
    the same way it round-trips coords."""
    fixture = tmp_path / "precision.yaml"
    fixture.write_text(
        """
must_see:
  - name: My Tho Coconut Candy Villages
    area: Mekong Delta
    what: A cluster of candy workshops near My Tho.
    why: Confirms location_precision survives a reload intact.
    confidence: high
    geocode_query: My Tho Coconut Candy Villages, Vietnam
    coords:
      lat: 10.35
      lng: 106.36
    location_precision: approximate
""",
        encoding="utf-8",
    )
    records = load_records(str(fixture))
    assert len(records) == 1
    assert records[0].location_precision == "approximate"
    assert records[0].lat == 10.35


def test_persist_writes_location_precision_for_approximate_hits(tmp_path, monkeypatch):
    monkeypatch.setattr(cli_module, "DATA_DIR", str(tmp_path))
    path = tmp_path / "hanoi.yaml"
    path.write_text(
        "must_see:\n"
        "- name: Test Place\n"
        "  area: Old Quarter\n"
        "  what: w\n"
        "  why: w2\n"
        "  confidence: high\n"
        "  geocode_query: Test Place, Hanoi, Vietnam\n",
        encoding="utf-8",
    )
    rec = Record(name="Test Place", category="must_see", area="Old Quarter",
                 what="w", why="w2", confidence="high",
                 geocode_query="Test Place, Hanoi, Vietnam")
    rec.lat, rec.lng = 21.03, 105.84
    rec.location_precision = "approximate"

    _persist("hanoi", [rec])

    saved = yaml.safe_load(path.read_text(encoding="utf-8"))
    entry = saved["must_see"][0]
    assert entry["coords"] == {"lat": 21.03, "lng": 105.84}
    assert entry["location_precision"] == "approximate"


def test_load_records_round_trips_the_optional_video_field(tmp_path):
    fixture = tmp_path / "video.yaml"
    fixture.write_text(
        """
attractions:
  - name: Ha Long Bay Cruise
    area: Ha Long
    what: A day cruise through the limestone karsts of Ha Long Bay.
    why: Confirms load_records passes the optional video field through.
    confidence: high
    geocode_query: Ha Long Bay Cruise, Vietnam
    sources:
    - https://example.test/a
    video: https://www.youtube.com/watch?v=abc123
""",
        encoding="utf-8",
    )
    records = load_records(str(fixture))
    assert len(records) == 1
    assert records[0].video == "https://www.youtube.com/watch?v=abc123"


def test_persist_omits_location_precision_for_exact_hits(tmp_path, monkeypatch):
    """Exact hits keep the YAML quiet: no location_precision key at all,
    and a stale one from an earlier fallback run is cleared on rewrite."""
    monkeypatch.setattr(cli_module, "DATA_DIR", str(tmp_path))
    path = tmp_path / "hanoi.yaml"
    path.write_text(
        "must_see:\n"
        "- name: Test Place\n"
        "  area: Old Quarter\n"
        "  what: w\n"
        "  why: w2\n"
        "  confidence: high\n"
        "  geocode_query: Test Place, Hanoi, Vietnam\n"
        "  location_precision: approximate\n",
        encoding="utf-8",
    )
    rec = Record(name="Test Place", category="must_see", area="Old Quarter",
                 what="w", why="w2", confidence="high",
                 geocode_query="Test Place, Hanoi, Vietnam")
    rec.lat, rec.lng = 21.03, 105.84
    rec.location_precision = None

    _persist("hanoi", [rec])

    saved = yaml.safe_load(path.read_text(encoding="utf-8"))
    entry = saved["must_see"][0]
    assert entry["coords"] == {"lat": 21.03, "lng": 105.84}
    assert "location_precision" not in entry


# --- 12-01: a hand-verified pin survives the geocode stage ---------------

_PLACES = """
places:
  - { id: hanoi, name: Hanoi, region: north, lat: 21.0285, lng: 105.8522, radius_km: 30 }
"""

_LOCKED = """
restaurants:
- name: Locked Place
  area: Dong Da, 61 Van Mieu
  what: A restaurant whose pin was verified by hand.
  why: Pins the coords_manual lock against the geocoder.
  confidence: high
  geocode_query: Wrong Query, Hanoi, Vietnam
  coords_manual: true
  coords:
    lat: 21.029
    lng: 105.836
  sources:
  - https://example.test/a
- name: Free Place
  area: Old Quarter
  what: A restaurant geocoded the normal way.
  why: Shows the lock does not stop ordinary geocoding.
  confidence: high
  geocode_query: Free Place, Hanoi, Vietnam
  sources:
  - https://example.test/b
"""


def _geocode_setup(tmp_path, monkeypatch):
    data = tmp_path / "data"
    data.mkdir()
    (data / "places.yaml").write_text(_PLACES, encoding="utf-8")
    (data / "hanoi.yaml").write_text(_LOCKED, encoding="utf-8")
    monkeypatch.setattr(cli_module, "DATA_DIR", str(data))
    monkeypatch.setattr(cli_module, "write_review_queue", lambda *a, **k: None)
    calls = []

    class FakeResult:
        accepted = True
        lat, lng, precision = 21.0, 105.8, "exact"

    class FakeGeocoder:
        def __init__(self, *_a, **_k):
            pass

        def resolve(self, rec, place):
            calls.append(rec.name)
            return FakeResult()

    monkeypatch.setattr(cli_module, "Geocoder", FakeGeocoder)
    return data, calls


def test_geocode_skips_a_manually_locked_pin(tmp_path, monkeypatch):
    data, calls = _geocode_setup(tmp_path, monkeypatch)
    assert cli_module.cmd_geocode() == 0
    assert "Locked Place" not in calls
    raw = yaml.safe_load((data / "hanoi.yaml").read_text(encoding="utf-8"))
    locked = raw["restaurants"][0]
    assert locked["coords"] == {"lat": 21.029, "lng": 105.836}
    assert locked["coords_manual"] is True


def test_geocode_still_resolves_unlocked_records(tmp_path, monkeypatch):
    data, calls = _geocode_setup(tmp_path, monkeypatch)
    cli_module.cmd_geocode()
    assert calls == ["Free Place"]
    raw = yaml.safe_load((data / "hanoi.yaml").read_text(encoding="utf-8"))
    assert raw["restaurants"][1]["coords"] == {"lat": 21.0, "lng": 105.8}


def test_coords_manual_is_loaded_into_the_record(tmp_path, monkeypatch):
    data, _ = _geocode_setup(tmp_path, monkeypatch)
    recs = load_records(str(data / "hanoi.yaml"))
    assert recs[0].coords_manual is True and recs[1].coords_manual is False
