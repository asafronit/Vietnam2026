from kmlpool.cli import load_records


def test_loads_records_across_categories():
    records = load_records("data/hanoi.yaml")
    categories = {r.category for r in records}
    assert categories == {"hotels", "must_see", "food"}


def test_category_is_taken_from_the_yaml_key():
    records = load_records("data/hanoi.yaml")
    hotel = next(r for r in records if r.name.startswith("Peridot"))
    assert hotel.category == "hotels"
    assert hotel.tier == 5


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
