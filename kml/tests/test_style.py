import pytest
from kmlpool.style import to_kml_color, PLACE_COLORS, ICON_HREFS, style_id
from kmlpool.schema import CATEGORIES


def test_pure_red_becomes_alpha_blue_green_red():
    # #ff0000 is red. In aabbggrr that is ff 00 00 ff.
    assert to_kml_color("#ff0000") == "ff0000ff"


def test_pure_blue_becomes_alpha_blue_green_red():
    assert to_kml_color("#0000ff") == "ffff0000"


def test_pure_green_is_unchanged_in_the_middle():
    assert to_kml_color("#00ff00") == "ff00ff00"


def test_accepts_hex_without_the_hash():
    assert to_kml_color("ff0000") == "ff0000ff"


def test_alpha_is_configurable():
    assert to_kml_color("#ff0000", alpha="80") == "800000ff"


def test_rejects_malformed_hex():
    with pytest.raises(ValueError):
        to_kml_color("#ff00")


def test_every_place_has_a_colour():
    expected = {
        "hanoi", "ha-giang", "sapa", "ha-long", "ninh-binh",
        "phong-nha", "hue", "hoi-an",
        "buon-ma-thuot", "lak-lake", "da-lat",
        "saigon", "mekong", "phu-quoc",
    }
    assert set(PLACE_COLORS) == expected


def test_place_colours_are_distinct():
    assert len(set(PLACE_COLORS.values())) == len(PLACE_COLORS)


def test_every_category_has_an_icon():
    assert set(ICON_HREFS) == set(CATEGORIES)


def test_style_id_is_stable_and_xml_safe():
    assert style_id("ha-giang", "must_see") == "s-ha-giang-must_see"


def test_hotel_style_id_encodes_the_tier():
    from kmlpool.style import hotel_style_id
    assert hotel_style_id("hanoi", 5, avoid=False) == "s-hanoi-hotels-t5"


def test_avoided_hotels_get_their_own_style():
    from kmlpool.style import hotel_style_id
    assert hotel_style_id("sapa", 4, avoid=True) == "s-sapa-hotels-avoid"


def test_higher_tiers_get_bigger_pins():
    from kmlpool.style import HOTEL_TIER_SCALES
    assert HOTEL_TIER_SCALES[5] > HOTEL_TIER_SCALES[4] > HOTEL_TIER_SCALES[3]


def test_avoid_color_is_not_reused_from_the_place_palette():
    from kmlpool.style import AVOID_COLOR
    assert AVOID_COLOR not in PLACE_COLORS.values()
