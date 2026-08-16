import pytest

from kmlpool.verify import haversine_km, verify_kml, verify_within_radius
from kmlpool.inventory import Place
from kmlpool.schema import Record

MINIMAL = b"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>T</name>
<Folder><name>Food</name>
<Placemark><name>A</name><Point><coordinates>105.8,21.0,0</coordinates></Point></Placemark>
</Folder></Document></kml>"""

OUT_OF_COUNTRY = MINIMAL.replace(b"105.8,21.0", b"2.35,48.85")  # Paris


def test_haversine_hanoi_to_sapa_is_about_260_km():
    assert 240 < haversine_km(21.0285, 105.8522, 22.3364, 103.8440) < 280


def test_haversine_of_a_point_to_itself_is_zero():
    assert haversine_km(21.0, 105.0, 21.0, 105.0) == pytest.approx(0.0, abs=1e-6)


def test_clean_kml_has_no_errors():
    assert verify_kml(MINIMAL) == []


def test_coordinates_outside_vietnam_are_caught():
    errs = verify_kml(OUT_OF_COUNTRY)
    assert any("outside Vietnam" in e for e in errs)


def test_too_many_layers_is_caught():
    folders = b"".join(
        b"<Folder><name>L%d</name></Folder>" % i for i in range(11)
    )
    xml = (b'<?xml version="1.0" encoding="UTF-8"?>'
           b'<kml xmlns="http://www.opengis.net/kml/2.2"><Document>'
           + folders + b"</Document></kml>")
    assert any("layers" in e for e in verify_kml(xml))


def test_oversized_file_is_caught():
    padding = b"<!--" + b"x" * (6 * 1024 * 1024) + b"-->"
    assert any("5MB" in e for e in verify_kml(MINIMAL + padding))


def test_point_beyond_the_place_radius_is_caught():
    hanoi = Place("hanoi", "Hanoi", "north", 21.0285, 105.8522, 30)
    far = Record(name="Wrong", category="food", area="?", what="w", why="w2",
                 confidence="high", geocode_query="q", sources=["https://a"])
    far.lat, far.lng = 22.3364, 103.8440  # Sapa, 260 km away
    errs = verify_within_radius([hanoi], {"hanoi": [far]})
    assert any("Wrong" in e and "30 km" in e for e in errs)


def test_entity_expansion_does_not_blow_up_the_parser():
    """Billion laughs. The hardened parser must not expand this."""
    bomb = (b'<?xml version="1.0"?>'
            b'<!DOCTYPE kml ['
            b'<!ENTITY a "aaaaaaaaaa">'
            b'<!ENTITY b "&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;">'
            b'<!ENTITY c "&b;&b;&b;&b;&b;&b;&b;&b;&b;&b;">'
            b']>'
            b'<kml xmlns="http://www.opengis.net/kml/2.2"><Document>'
            b'<name>&c;</name></Document></kml>')
    errors = verify_kml(bomb)  # must return, not hang or exhaust memory
    assert isinstance(errors, list)


def test_point_inside_the_wide_ha_giang_radius_passes():
    ha_giang = Place("ha-giang", "Ha Giang", "north", 22.8278, 104.9839, 120)
    on_loop = Record(name="Ma Pi Leng", category="must_see", area="?", what="w", why="w2",
                     confidence="high", geocode_query="q", sources=["https://a"])
    on_loop.lat, on_loop.lng = 23.2500, 105.3300
    assert verify_within_radius([ha_giang], {"ha-giang": [on_loop]}) == []
