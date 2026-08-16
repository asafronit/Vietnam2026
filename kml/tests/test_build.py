import lxml.etree as ET

from kmlpool.build import build_pool_kml
from kmlpool.inventory import Place
from kmlpool.schema import Record

NS = {"k": "http://www.opengis.net/kml/2.2"}


def place(pid="hanoi", region="north"):
    return Place(id=pid, name="Hanoi", region=region,
                 lat=21.0285, lng=105.8522, radius_km=30)


def rec(category="food", name="Bun Cha", conf="high", lat=21.0, lng=105.8):
    r = Record(
        name=name, category=category, area="Hai Ba Trung",
        what="A plain three-storey shop grilling pork over charcoal.",
        why="Michelin Bib Gourmand",
        confidence=conf, geocode_query=f"{name}, Hanoi, Vietnam",
        sources=["https://guide.michelin.com/x", "https://b.example/y"],
    )
    r.lat, r.lng = lat, lng
    if category == "hotels":
        r.tier, r.tier_official = 5, True
        r.price_low, r.price_high, r.price_checked = 80.0, 137.0, "2026-08-16"
    return r


def parse(xml_bytes):
    return ET.fromstring(xml_bytes)


def layer_names(xml_bytes):
    return [e.text for e in parse(xml_bytes).findall(".//k:Folder/k:name", NS)]


def pin_names(xml_bytes):
    return [e.text for e in parse(xml_bytes).findall(".//k:Placemark/k:name", NS)]


def test_output_is_well_formed_kml():
    doc = parse(build_pool_kml([place()], {"hanoi": [rec()]}))
    assert doc.tag == "{http://www.opengis.net/kml/2.2}kml"


def test_places_and_route_is_always_the_first_layer():
    assert layer_names(build_pool_kml([place()], {"hanoi": [rec()]}))[0] == "Places & Route"


def test_one_layer_per_category_that_has_records():
    xml = build_pool_kml([place()], {"hanoi": [rec("food"), rec("hotels", "Peridot")]})
    assert layer_names(xml) == ["Places & Route", "Hotels", "Food"]


def test_empty_categories_produce_no_layer():
    xml = build_pool_kml([place()], {"hanoi": [rec("food")]})
    assert layer_names(xml) == ["Places & Route", "Food"]


def test_a_full_map_has_exactly_seven_layers():
    recs = [rec(c, f"r-{c}") for c in
            ("hotels", "must_see", "attractions", "food", "markets", "logistics")]
    assert len(layer_names(build_pool_kml([place()], {"hanoi": recs}))) == 7


def test_places_layer_holds_one_pin_per_place_plus_the_route():
    places = [place("hanoi", "north"), place("phu-quoc", "south")]
    doc = parse(build_pool_kml(places, {}))
    layer = doc.findall(".//k:Folder", NS)[0]
    assert len(layer.findall("k:Placemark/k:Point", NS)) == 2
    assert len(layer.findall("k:Placemark/k:LineString", NS)) == 1


def test_every_region_lands_in_the_same_file():
    north, south = place("hanoi", "north"), place("phu-quoc", "south")
    xml = build_pool_kml([north, south],
                         {"hanoi": [rec(name="N")], "phu-quoc": [rec(name="S")]})
    assert "N" in pin_names(xml) and "S" in pin_names(xml)


def test_low_confidence_records_are_excluded():
    xml = build_pool_kml([place()],
                         {"hanoi": [rec(name="Good"), rec(name="Bad", conf="low")]})
    assert "Bad" not in pin_names(xml) and "Good" in pin_names(xml)


def test_ungeocoded_records_are_excluded():
    r = rec(name="NoCoords")
    r.lat, r.lng = None, None
    xml = build_pool_kml([place()], {"hanoi": [rec(name="Fine"), r]})
    assert "NoCoords" not in pin_names(xml) and "Fine" in pin_names(xml)


def test_coordinates_are_written_longitude_first():
    xml = build_pool_kml([place()], {"hanoi": [rec(lat=21.0, lng=105.8)]})
    coords = parse(xml).findall(".//k:Point/k:coordinates", NS)[-1].text
    assert coords.startswith("105.8,21.0")


def test_description_is_wrapped_in_cdata_with_a_source_link():
    xml = build_pool_kml([place()], {"hanoi": [rec()]})
    assert b"<![CDATA[" in xml
    assert b"guide.michelin.com" in xml


def test_every_pin_explains_what_it_is_and_why_it_is_listed():
    xml = build_pool_kml([place()], {"hanoi": [rec()]})
    assert b"grilling pork over charcoal" in xml      # what
    assert b"Why it&#39;s here:" in xml or b"Why it's here:" in xml
    assert b"Michelin Bib" in xml                     # why


def test_hotel_description_shows_indicative_price_and_check_date():
    xml = build_pool_kml([place()], {"hanoi": [rec("hotels", "Peridot")]})
    assert b"indicative" in xml
    assert b"2026-08-16" in xml


def test_hotel_over_two_hundred_at_the_top_end_is_flagged():
    r = rec("hotels", "Wide Range")
    r.price_low, r.price_high = 180.0, 350.0
    xml = build_pool_kml([place()], {"hanoi": [r]})
    assert b"upper room types exceed" in xml


def test_hotel_pins_reference_their_tier_style():
    xml = build_pool_kml([place()], {"hanoi": [rec("hotels", "Peridot")]})
    assert b"#s-hanoi-hotels-t5" in xml


def test_avoided_hotels_are_flagged_and_use_the_warning_style():
    r = rec("hotels", "Bamboo Sapa")
    r.avoid = True
    xml = build_pool_kml([place()], {"hanoi": [r]})
    assert b"#s-hanoi-hotels-avoid" in xml
    assert b"AVOID" in xml


def test_no_hebrew_reaches_the_output():
    xml = build_pool_kml([place()], {"hanoi": [rec()]})
    assert not any(0x0590 <= ord(c) <= 0x05FF for c in xml.decode("utf-8"))
