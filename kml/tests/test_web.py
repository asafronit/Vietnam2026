"""Tests for the `web` command: out/poi-data.js for the PWA map page.

Fixtures own their own places.yaml (mirroring data/places.yaml's structural
facts -- id/name/region/lat/lng/radius_km) and their own per-place records,
never the real research YAML, so these tests do not break when the research
content in data/*.yaml is edited.
"""
import json
import os

import kmlpool.cli as cli_module
from kmlpool.cli import cmd_web
from kmlpool.style import PLACE_COLORS

PLACES_YAML = """
places:
  - { id: hanoi,          name: Hanoi,               region: north,     lat: 21.0285, lng: 105.8522, radius_km: 30 }
  - { id: ha-giang,       name: Ha Giang,            region: north,     lat: 22.8278, lng: 104.9839, radius_km: 120 }
  - { id: sapa,           name: Sapa,                region: north,     lat: 22.3364, lng: 103.8440, radius_km: 30 }
  - { id: ha-long,        name: Ha Long and Cat Ba,  region: north,     lat: 20.9099, lng: 107.1839, radius_km: 50 }
  - { id: ninh-binh,      name: Ninh Binh,           region: north,     lat: 20.2505, lng: 105.9745, radius_km: 30 }
  - { id: phong-nha,      name: Phong Nha,           region: central,   lat: 17.5934, lng: 106.2865, radius_km: 30 }
  - { id: hue,            name: Hue,                 region: central,   lat: 16.4637, lng: 107.5909, radius_km: 30 }
  - { id: hoi-an,         name: Hoi An and Da Nang,  region: central,   lat: 15.8801, lng: 108.3380, radius_km: 40 }
  - { id: buon-ma-thuot,  name: Buon Ma Thuot,       region: highlands, lat: 12.6797, lng: 108.0378, radius_km: 30 }
  - { id: lak-lake,       name: Lak Lake,            region: highlands, lat: 12.4076, lng: 108.1836, radius_km: 30 }
  - { id: da-lat,         name: Da Lat,              region: highlands, lat: 11.9404, lng: 108.4583, radius_km: 30 }
  - { id: saigon,         name: Ho Chi Minh City,    region: south,     lat: 10.7769, lng: 106.7009, radius_km: 40 }
  - { id: mekong,         name: Mekong and Can Tho,  region: south,     lat: 10.0452, lng: 105.7469, radius_km: 80 }
  - { id: phu-quoc,       name: Phu Quoc,            region: south,     lat: 10.2899, lng: 103.9840, radius_km: 40 }
"""

HANOI_YAML = """
must_see:
  - name: Good Lake
    area: Old Quarter
    what: A lake used only as a fixture for the web export tests.
    why: Confirms a high-confidence geocoded record is shipped.
    confidence: high
    geocode_query: Good Lake, Hanoi, Vietnam
    sources:
    - https://example.test/a
    coords:
      lat: 21.03
      lng: 105.84
  - name: Bad Lake
    area: Old Quarter
    what: A lake used only as a fixture for the web export tests.
    why: Confirms a low-confidence record is excluded from the export.
    confidence: low
    geocode_query: Bad Lake, Hanoi, Vietnam
    sources:
    - https://example.test/b
    coords:
      lat: 21.04
      lng: 105.85
  - name: No Coords Lake
    area: Old Quarter
    what: A lake used only as a fixture for the web export tests.
    why: Confirms an ungeocoded record is excluded from the export.
    confidence: high
    geocode_query: No Coords Lake, Hanoi, Vietnam
    sources:
    - https://example.test/c
hotels:
  - name: Approx Hotel
    tier: 4
    tier_official: false
    price_low: 45
    price_high: 60
    price_checked: '2026-08-16'
    area: Old Quarter
    what: A hotel used only as a fixture for the web export tests.
    why: Confirms camelCase field mapping and the approximate flag.
    confidence: high
    geocode_query: Approx Hotel, Hanoi, Vietnam
    sources:
    - https://example.test/d
    - https://example.test/e
    coords:
      lat: 21.05
      lng: 105.86
    location_precision: approximate
"""

INVALID_HANOI_YAML = """
must_see:
  - name: Broken Place
    area: Old Quarter
    what: A place with a missing why field, used to trip validation.
    why: ''
    confidence: high
    geocode_query: Broken Place, Hanoi, Vietnam
    sources:
    - https://example.test/a
"""


def _setup(tmp_path, monkeypatch, hanoi_yaml=HANOI_YAML):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "places.yaml").write_text(PLACES_YAML, encoding="utf-8")
    if hanoi_yaml is not None:
        (data_dir / "hanoi.yaml").write_text(hanoi_yaml, encoding="utf-8")
    out_dir = tmp_path / "out"
    monkeypatch.setattr(cli_module, "DATA_DIR", str(data_dir))
    monkeypatch.setattr(cli_module, "OUT_DIR", str(out_dir))
    return out_dir


def _run_and_load(tmp_path, monkeypatch, hanoi_yaml=HANOI_YAML):
    out_dir = _setup(tmp_path, monkeypatch, hanoi_yaml)
    rc = cmd_web()
    assert rc == 0
    raw = (out_dir / "poi-data.js").read_text(encoding="utf-8")
    prefix = "const POI_DATA = "
    assert raw.startswith(prefix)
    assert raw.endswith(";\n")
    data = json.loads(raw[len(prefix):-2])
    return data


def test_web_writes_poi_data_js_with_const_prefix(tmp_path, monkeypatch):
    out_dir = _setup(tmp_path, monkeypatch)
    rc = cmd_web()
    assert rc == 0
    raw = (out_dir / "poi-data.js").read_text(encoding="utf-8")
    assert raw.startswith("const POI_DATA = ")


def test_output_parses_as_valid_json_once_stripped(tmp_path, monkeypatch):
    data = _run_and_load(tmp_path, monkeypatch)
    assert isinstance(data, dict)


def test_all_14_places_present_keyed_by_id_with_seq_1_to_14(tmp_path, monkeypatch):
    data = _run_and_load(tmp_path, monkeypatch)
    expected_ids = [
        "hanoi", "ha-giang", "sapa", "ha-long", "ninh-binh", "phong-nha",
        "hue", "hoi-an", "buon-ma-thuot", "lak-lake", "da-lat", "saigon",
        "mekong", "phu-quoc",
    ]
    assert set(data.keys()) == set(expected_ids)
    for i, place_id in enumerate(expected_ids, start=1):
        assert data[place_id]["seq"] == i


def test_low_confidence_record_is_excluded(tmp_path, monkeypatch):
    data = _run_and_load(tmp_path, monkeypatch)
    names = [r["name"] for r in data["hanoi"]["poi"]["must_see"]]
    assert "Bad Lake" not in names


def test_high_confidence_geocoded_record_is_included(tmp_path, monkeypatch):
    data = _run_and_load(tmp_path, monkeypatch)
    names = [r["name"] for r in data["hanoi"]["poi"]["must_see"]]
    assert "Good Lake" in names


def test_ungeocoded_record_still_reaches_the_web_pool(tmp_path, monkeypatch):
    """The web gate deliberately does not require coordinates.

    KML is a map format, so a pin without coordinates is meaningless there and
    `is_shippable` still blocks it. A web card is not: it can carry the name,
    the description and the reason, and link out to a maps *search*. Requiring
    coordinates here was inherited from the KML path by accident and was
    silently withholding roughly half the researched records from the site.
    """
    data = _run_and_load(tmp_path, monkeypatch)
    names = [r["name"] for r in data["hanoi"]["poi"]["must_see"]]
    assert "No Coords Lake" in names


def test_ungeocoded_record_carries_no_coordinates(tmp_path, monkeypatch):
    """Shipping it is not the same as inventing a location for it."""
    data = _run_and_load(tmp_path, monkeypatch)
    lake = next(
        r for r in data["hanoi"]["poi"]["must_see"] if r["name"] == "No Coords Lake"
    )
    assert lake.get("lat") is None
    assert lake.get("lng") is None


def test_counts_matches_actual_length_of_category_arrays(tmp_path, monkeypatch):
    data = _run_and_load(tmp_path, monkeypatch)
    hanoi = data["hanoi"]
    for category, records in hanoi["poi"].items():
        assert hanoi["counts"][category] == len(records)
    # Good Lake and No Coords Lake both ship; Bad Lake is low-confidence and
    # is the only must_see the web gate rejects.
    assert hanoi["counts"]["must_see"] == 2
    assert hanoi["counts"]["hotels"] == 1


def test_approx_is_true_for_approximate_location_precision(tmp_path, monkeypatch):
    data = _run_and_load(tmp_path, monkeypatch)
    hotel = next(r for r in data["hanoi"]["poi"]["hotels"] if r["name"] == "Approx Hotel")
    assert hotel["approx"] is True
    lake = next(r for r in data["hanoi"]["poi"]["must_see"] if r["name"] == "Good Lake")
    assert lake["approx"] is False


def test_color_matches_style_place_colors(tmp_path, monkeypatch):
    data = _run_and_load(tmp_path, monkeypatch)
    for place_id, place_data in data.items():
        assert place_data["color"] == PLACE_COLORS[place_id]


def test_camelcase_mapping_price_low_becomes_pricelow(tmp_path, monkeypatch):
    data = _run_and_load(tmp_path, monkeypatch)
    hotel = next(r for r in data["hanoi"]["poi"]["hotels"] if r["name"] == "Approx Hotel")
    assert hotel["priceLow"] == 45
    assert hotel["priceHigh"] == 60
    assert hotel["priceChecked"] == "2026-08-16"
    assert hotel["tierOfficial"] is False
    assert "price_low" not in hotel
    assert "tier_official" not in hotel


def test_null_fields_are_always_present_even_when_absent(tmp_path, monkeypatch):
    data = _run_and_load(tmp_path, monkeypatch)
    lake = next(r for r in data["hanoi"]["poi"]["must_see"] if r["name"] == "Good Lake")
    assert lake["tier"] is None
    assert lake["kind"] is None
    assert lake["signal"] is None
    assert lake["video"] is None
    assert lake["avoid"] is False


def test_command_exits_nonzero_and_writes_nothing_on_invalid_record(tmp_path, monkeypatch, capsys):
    out_dir = _setup(tmp_path, monkeypatch, hanoi_yaml=INVALID_HANOI_YAML)
    rc = cmd_web()
    assert rc != 0
    captured = capsys.readouterr()
    assert "INVALID" in captured.err
    assert not os.path.exists(out_dir / "poi-data.js")
