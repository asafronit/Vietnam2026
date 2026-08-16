import pytest
from kmlpool.inventory import load_places, Place

PLACES = "data/places.yaml"


def test_loads_fourteen_places():
    places = load_places(PLACES)
    assert len(places) == 14


def test_ids_are_unique():
    ids = [p.id for p in load_places(PLACES)]
    assert len(ids) == len(set(ids))


def test_regions_are_the_four_known_ones():
    regions = {p.region for p in load_places(PLACES)}
    assert regions == {"north", "central", "highlands", "south"}


def test_every_anchor_is_inside_vietnam():
    for p in load_places(PLACES):
        assert 8.2 <= p.lat <= 23.4, f"{p.id} latitude out of Vietnam"
        assert 102.1 <= p.lng <= 109.5, f"{p.id} longitude out of Vietnam"


def test_ha_giang_has_the_wide_loop_radius():
    ha_giang = next(p for p in load_places(PLACES) if p.id == "ha-giang")
    assert ha_giang.radius_km == 120


def test_rejects_duplicate_ids(tmp_path):
    bad = tmp_path / "dup.yaml"
    bad.write_text(
        "places:\n"
        "  - { id: x, name: X, region: north, lat: 21.0, lng: 105.0, radius_km: 30 }\n"
        "  - { id: x, name: Y, region: south, lat: 10.0, lng: 106.0, radius_km: 30 }\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate place id"):
        load_places(str(bad))
