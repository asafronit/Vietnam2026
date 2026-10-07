"""Tests for inter-city transfers: data/transfers/<from>__<to>.yaml -> out/transfers-data.js.

A transfer is not a point of interest -- it joins two stations and carries
several ways to make the trip (sleeper bus, night train, private car...). It
therefore lives in its own directory and its own output file, and never enters
POI_DATA's categories, counts, map or search.

Fixtures own their own places.yaml and transfer files, never the real research
YAML, so these tests do not break when data/transfers/*.yaml is edited.
"""
import copy
import json

import pytest
import yaml

import kmlpool.cli as cli_module
from kmlpool.cli import cmd_build, cmd_web

PLACES_YAML = """
places:
  - { id: hanoi,     name: Hanoi,     region: north, lat: 21.0285, lng: 105.8522, radius_km: 30 }
  - { id: sapa,      name: Sapa,      region: north, lat: 22.3364, lng: 103.8440, radius_km: 30 }
  - { id: ninh-binh, name: Ninh Binh, region: north, lat: 20.2505, lng: 105.9745, radius_km: 30 }
"""

PREFIX = "const TRANSFERS_DATA = "


def _option(**overrides) -> dict:
    opt = {
        "mode": "sleeper_bus",
        "operator": "Good Bus Co",
        "board": {
            "name": "Good Bus office",
            "address": "1 Test Street, Hoan Kiem, Hanoi",
            "lat": 21.03,
            "lng": 105.85,
        },
        "departures": "07:00, 22:00",
        "departures_he": "07:00, 22:00",
        "op_lang": "en",
        "duration_min": 330,
        "duration_max": 360,
        "price_low": 450000,
        "price_high": 600000,
        "currency": "VND",
        "price_unit": "per_person",
        "book_links": [{"name": "Good Bus Co", "url": "https://example.test/book"}],
        "pros": ["Door to door"],
        "pros_he": ["מדלת לדלת"],
        "cons": ["Winding road"],
        "cons_he": ["דרך מפותלת"],
        "tips": "Book the front cabins.",
        "tips_he": "להזמין את התאים הקדמיים.",
        "sources": ["https://example.test/source"],
        "checked": "2026-10-06",
        "confidence": "high",
    }
    opt.update(overrides)
    return opt


def _transfer(**overrides) -> dict:
    t = {
        "from": "hanoi",
        "to": "sapa",
        "reverse_ok": True,
        "options": [_option()],
    }
    t.update(overrides)
    return t


def _setup(tmp_path, monkeypatch, transfers: dict[str, dict] | None = None):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "places.yaml").write_text(PLACES_YAML, encoding="utf-8")
    if transfers is not None:
        tdir = data_dir / "transfers"
        tdir.mkdir()
        for filename, body in transfers.items():
            (tdir / filename).write_text(
                yaml.safe_dump(body, allow_unicode=True, sort_keys=False), encoding="utf-8"
            )
    out_dir = tmp_path / "out"
    monkeypatch.setattr(cli_module, "DATA_DIR", str(data_dir))
    monkeypatch.setattr(cli_module, "OUT_DIR", str(out_dir))
    return out_dir


def _load_output(out_dir) -> list:
    raw = (out_dir / "transfers-data.js").read_text(encoding="utf-8")
    assert raw.startswith(PREFIX)
    assert raw.endswith(";\n")
    return json.loads(raw[len(PREFIX):-2])


def _run_ok(tmp_path, monkeypatch, transfers) -> list:
    out_dir = _setup(tmp_path, monkeypatch, transfers)
    assert cmd_web() == 0
    return _load_output(out_dir)


# --- AC-1: a valid transfer is exported -----------------------------------


def test_valid_transfer_is_written_with_const_prefix(tmp_path, monkeypatch):
    data = _run_ok(tmp_path, monkeypatch, {"hanoi__sapa.yaml": _transfer()})
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["from"] == "hanoi"
    assert data[0]["to"] == "sapa"
    assert data[0]["reverseOk"] is True


def test_option_is_mapped_to_camel_case_with_nested_board(tmp_path, monkeypatch):
    data = _run_ok(tmp_path, monkeypatch, {"hanoi__sapa.yaml": _transfer()})
    opt = data[0]["options"][0]
    assert opt["mode"] == "sleeper_bus"
    assert opt["operator"] == "Good Bus Co"
    assert opt["board"] == {
        "name": "Good Bus office",
        "address": "1 Test Street, Hoan Kiem, Hanoi",
        "pickupHotel": False,
        "lat": 21.03,
        "lng": 105.85,
        # The language the stop is written in, defaulting to en. The page sets
        # it as a lang attribute, so a Hebrew screen reader does not voice an
        # English sentence with Vietnamese phonemes.
        "lang": "en",
    }
    assert opt["alight"] is None
    assert opt["durationMin"] == 330
    assert opt["durationMax"] == 360
    assert opt["priceLow"] == 450000
    assert opt["priceHigh"] == 600000
    assert opt["currency"] == "VND"
    assert opt["priceUnit"] == "per_person"
    assert opt["bookLinks"] == [{"name": "Good Bus Co", "url": "https://example.test/book"}]
    assert opt["prosHe"] == ["מדלת לדלת"]
    assert opt["consHe"] == ["דרך מפותלת"]
    assert opt["tipsHe"] == "להזמין את התאים הקדמיים."
    assert opt["checked"] == "2026-10-06"
    assert opt["sources"] == ["https://example.test/source"]


def test_exported_option_has_exactly_the_contract_keys(tmp_path, monkeypatch):
    """Explicit mapping: a future model field must not leak into the page."""
    data = _run_ok(tmp_path, monkeypatch, {"hanoi__sapa.yaml": _transfer()})
    assert set(data[0]["options"][0]) == {
        "mode", "operator", "opLang", "board", "alight", "departures", "departuresHe",
        "durationMin", "durationMax", "priceLow", "priceHigh", "currency",
        "priceUnit", "bookLinks", "pros", "prosHe", "cons", "consHe",
        "tips", "tipsHe", "sources", "checked", "confidence",
    }
    assert set(data[0]) == {"from", "to", "reverseOk", "note", "noteHe", "options"}


def test_hotel_pickup_board_needs_no_coordinates(tmp_path, monkeypatch):
    board = {"name": "Hotel pickup", "address": "Old Quarter hotels", "pickup_hotel": True}
    data = _run_ok(
        tmp_path, monkeypatch, {"hanoi__sapa.yaml": _transfer(options=[_option(board=board)])}
    )
    assert data[0]["options"][0]["board"]["pickupHotel"] is True
    assert data[0]["options"][0]["board"]["lat"] is None


def test_poi_data_is_still_written(tmp_path, monkeypatch):
    out_dir = _setup(tmp_path, monkeypatch, {"hanoi__sapa.yaml": _transfer()})
    assert cmd_web() == 0
    raw = (out_dir / "poi-data.js").read_text(encoding="utf-8")
    assert raw.startswith("const POI_DATA = ")
    assert "transfers" not in json.loads(raw[len("const POI_DATA = "):-2])["hanoi"]["poi"]


def test_transfers_sorted_by_filename_for_stable_output(tmp_path, monkeypatch):
    data = _run_ok(
        tmp_path,
        monkeypatch,
        {
            "sapa__ninh-binh.yaml": _transfer(**{"from": "sapa", "to": "ninh-binh"}),
            "hanoi__sapa.yaml": _transfer(),
        },
    )
    assert [(t["from"], t["to"]) for t in data] == [("hanoi", "sapa"), ("sapa", "ninh-binh")]


# --- AC-2: invalid data fails the build and writes nothing ----------------


def _set(path: str, value):
    """Return a mutator that sets a dotted path on the first option/transfer."""
    def mutate(t: dict) -> dict:
        t = copy.deepcopy(t)
        keys = path.split(".")
        target = t
        if keys[0] == "opt":
            target = t["options"][0]
            keys = keys[1:]
        for k in keys[:-1]:
            target = target[k]
        if value is _DELETE:
            target.pop(keys[-1], None)
        else:
            target[keys[-1]] = value
        return t
    return mutate


_DELETE = object()

INVALID_CASES = {
    "unknown_from": (_set("from", "atlantis"), "from"),
    "unknown_to": (_set("to", "atlantis"), "to"),
    "same_from_to": (_set("to", "hanoi"), "same"),
    "no_options": (_set("options", []), "option"),
    "bad_mode": (_set("opt.mode", "teleport"), "mode"),
    "bad_currency": (_set("opt.currency", "EUR"), "currency"),
    "bad_price_unit": (_set("opt.price_unit", "per_dish"), "price_unit"),
    "bad_confidence": (_set("opt.confidence", "sure"), "confidence"),
    "missing_board": (_set("opt.board", _DELETE), "board"),
    "empty_address": (_set("opt.board.address", " "), "address"),
    "missing_lat_for_grab": (_set("opt.board.lat", _DELETE), "lat"),
    "lat_outside_vietnam": (_set("opt.board.lat", 48.85), "lat"),
    "lng_outside_vietnam": (_set("opt.board.lng", 2.35), "lng"),
    "missing_price_low": (_set("opt.price_low", _DELETE), "price_low"),
    "price_high_below_low": (_set("opt.price_high", 100), "price_high"),
    "duration_max_below_min": (_set("opt.duration_max", 60), "duration_max"),
    "missing_duration_min": (_set("opt.duration_min", _DELETE), "duration_min"),
    "missing_checked": (_set("opt.checked", _DELETE), "checked"),
    "checked_not_iso": (_set("opt.checked", "6/10/2026"), "checked"),
    "no_sources": (_set("opt.sources", []), "source"),
    "book_link_not_https": (
        _set("opt.book_links", [{"name": "X", "url": "http://example.test"}]), "book_links"
    ),
    "book_link_without_name": (
        _set("opt.book_links", [{"name": " ", "url": "https://example.test"}]), "book_links"
    ),
    # Asaf's standing rule: never price or book Vietjet.
    "vietjet_operator": (_set("opt.operator", "VietJet Air"), "Vietjet"),
    "vietjet_link": (
        _set("opt.book_links", [{"name": "Cheap", "url": "https://www.vietjetair.com"}]), "Vietjet"
    ),
    "pros_he_missing": (_set("opt.pros_he", _DELETE), "pros_he"),
    "pros_he_wrong_length": (_set("opt.pros_he", ["א", "ב"]), "pros_he"),
    "cons_he_missing": (_set("opt.cons_he", _DELETE), "cons_he"),
    "tips_without_hebrew": (_set("opt.tips_he", _DELETE), "tips_he"),
    "note_without_hebrew": (_set("note", "Book early."), "note_he"),
    "missing_operator": (_set("opt.operator", " "), "operator"),
    # 09-02: Hebrew departures are mandatory whenever departures exist,
    # and op_lang is a closed set so the page can trust it as a lang attribute.
    "departures_without_hebrew": (_set("opt.departures_he", _DELETE), "departures_he"),
    "bad_op_lang": (_set("opt.op_lang", "fr"), "op_lang"),
}


@pytest.mark.parametrize("case", sorted(INVALID_CASES))
def test_invalid_transfer_fails_web_and_writes_nothing(case, tmp_path, monkeypatch, capsys):
    mutate, needle = INVALID_CASES[case]
    out_dir = _setup(tmp_path, monkeypatch, {"hanoi__sapa.yaml": mutate(_transfer())})
    assert cmd_web() == 1
    err = capsys.readouterr().err
    assert "INVALID" in err
    assert "hanoi__sapa" in err or "transfers/" in err
    assert needle in err
    assert not (out_dir / "transfers-data.js").exists()
    assert not (out_dir / "poi-data.js").exists()


def test_error_names_the_option_index(tmp_path, monkeypatch, capsys):
    t = _transfer(options=[_option(), _option(currency="EUR")])
    _setup(tmp_path, monkeypatch, {"hanoi__sapa.yaml": t})
    assert cmd_web() == 1
    assert "option[1]" in capsys.readouterr().err


def test_duplicate_pair_in_two_files_fails(tmp_path, monkeypatch, capsys):
    out_dir = _setup(
        tmp_path,
        monkeypatch,
        {"hanoi__sapa.yaml": _transfer(), "hanoi__sapa-copy.yaml": _transfer()},
    )
    assert cmd_web() == 1
    assert "duplicate" in capsys.readouterr().err
    assert not (out_dir / "transfers-data.js").exists()


def test_invalid_transfer_also_blocks_kml_build(tmp_path, monkeypatch):
    """One source of truth for validity: build and web gate on the same checks."""
    _setup(tmp_path, monkeypatch, {"hanoi__sapa.yaml": _transfer(to="atlantis")})
    assert cmd_build() == 1


def test_flight_option_with_several_airline_links(tmp_path, monkeypatch):
    """A flight is boarded at the airport -- coordinates feed the Grab ride there --
    and is booked with whichever airline flies the route, so it carries one link each."""
    flight = _option(
        mode="flight",
        operator="Vietnam Airlines, Bamboo Airways",
        board={"name": "Noi Bai International Airport (HAN)", "address": "Phu Minh, Soc Son, Hanoi",
               "lat": 21.2187, "lng": 105.8042},
        book_links=[
            {"name": "Vietnam Airlines", "url": "https://www.vietnamairlines.com"},
            {"name": "Bamboo Airways", "url": "https://www.bambooairways.com"},
        ],
        currency="USD", price_low=60, price_high=120,
    )
    data = _run_ok(tmp_path, monkeypatch, {"hanoi__sapa.yaml": _transfer(options=[flight])})
    assert [l["name"] for l in data[0]["options"][0]["bookLinks"]] == ["Vietnam Airlines", "Bamboo Airways"]


def test_option_without_book_links_exports_empty_list(tmp_path, monkeypatch):
    opt = _option()
    del opt["book_links"]
    data = _run_ok(tmp_path, monkeypatch, {"hanoi__sapa.yaml": _transfer(options=[opt])})
    assert data[0]["options"][0]["bookLinks"] == []


# --- AC-3: low confidence never ships -------------------------------------


def test_low_confidence_option_is_dropped_others_kept(tmp_path, monkeypatch):
    t = _transfer(options=[_option(), _option(mode="train", confidence="low")])
    data = _run_ok(tmp_path, monkeypatch, {"hanoi__sapa.yaml": t})
    assert [o["mode"] for o in data[0]["options"]] == ["sleeper_bus"]


def test_transfer_with_only_low_confidence_options_is_dropped(tmp_path, monkeypatch):
    t = _transfer(options=[_option(confidence="low")])
    assert _run_ok(tmp_path, monkeypatch, {"hanoi__sapa.yaml": t}) == []


# --- AC-4: no transfers directory is not an error -------------------------


def test_missing_transfers_dir_writes_empty_array(tmp_path, monkeypatch):
    assert _run_ok(tmp_path, monkeypatch, None) == []


# --- 08-01 AC-1: an unknown key is reported, not a crash ------------------


@pytest.mark.parametrize(
    "mutate, key",
    [
        (lambda t: {**t, "reverse_okk": True}, "reverse_okk"),
        (lambda t: {**t, "options": [{**t["options"][0], "prise_low": 1}]}, "prise_low"),
        (
            lambda t: {
                **t,
                "options": [{**t["options"][0], "board": {**t["options"][0]["board"], "latt": 1}}],
            },
            "latt",
        ),
    ],
    ids=["transfer", "option", "board"],
)
def test_unknown_key_is_invalid_not_a_traceback(mutate, key, tmp_path, monkeypatch, capsys):
    out_dir = _setup(tmp_path, monkeypatch, {"hanoi__sapa.yaml": mutate(_transfer())})
    assert cmd_web() == 1
    err = capsys.readouterr().err
    assert "INVALID" in err
    assert "hanoi__sapa.yaml" in err
    assert key in err
    assert not (out_dir / "transfers-data.js").exists()


def test_yaml_syntax_error_is_invalid_not_a_traceback(tmp_path, monkeypatch, capsys):
    out_dir = _setup(tmp_path, monkeypatch, {})
    (tmp_path / "data" / "transfers" / "broken__file.yaml").write_text(
        "from: hanoi\nnote: plain text: with a colon\n  continues: here\n", encoding="utf-8"
    )
    assert cmd_web() == 1
    err = capsys.readouterr().err
    assert "INVALID" in err
    assert "broken__file.yaml" in err
    assert "YAML" in err
    assert not (out_dir / "transfers-data.js").exists()


# --- 09-02: departures_he and op_lang ------------------------------------


def test_departures_he_and_op_lang_are_exported(tmp_path, monkeypatch):
    opt = _option(departures="Daily 16:10", departures_he="כל יום 16:10", op_lang="vi")
    data = _run_ok(tmp_path, monkeypatch, {"hanoi__sapa.yaml": _transfer(options=[opt])})
    o = data[0]["options"][0]
    assert o["departuresHe"] == "כל יום 16:10"
    assert o["opLang"] == "vi"


def test_missing_op_lang_defaults_to_en(tmp_path, monkeypatch):
    opt = _option()
    del opt["op_lang"]
    data = _run_ok(tmp_path, monkeypatch, {"hanoi__sapa.yaml": _transfer(options=[opt])})
    assert data[0]["options"][0]["opLang"] == "en"


def test_no_departures_needs_no_hebrew_twin(tmp_path, monkeypatch):
    opt = _option()
    del opt["departures"]
    del opt["departures_he"]
    data = _run_ok(tmp_path, monkeypatch, {"hanoi__sapa.yaml": _transfer(options=[opt])})
    assert data[0]["options"][0]["departuresHe"] is None
