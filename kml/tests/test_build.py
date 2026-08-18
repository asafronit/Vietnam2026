import re

import lxml.etree as ET

from kmlpool.build import _description, build_place_kml, build_pool_kml
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


def test_approximate_location_gets_a_visible_note():
    r = rec()
    r.location_precision = "approximate"
    xml = build_pool_kml([place()], {"hanoi": [r]})
    assert b"Approximate location" in xml


def test_exact_location_has_no_approximate_note():
    xml = build_pool_kml([place()], {"hanoi": [rec()]})
    assert b"Approximate location" not in xml


def test_no_hebrew_reaches_the_output():
    xml = build_pool_kml([place()], {"hanoi": [rec()]})
    assert not any(0x0590 <= ord(c) <= 0x05FF for c in xml.decode("utf-8"))


# --- Directions link + raw coordinates (Task 11) ---------------------------
#
# grab:// deep links render as dead, unclickable text inside My Maps (it
# strips custom URI schemes). Replaced with a Google Maps directions URL
# (working) plus the raw coordinates as selectable plain text, since Grab
# itself can't be deep-linked to from inside My Maps — the traveller's path
# to a Grab ride is copying the coordinates into the Grab app by hand.

_DIRECTIONS_HREF_RE = re.compile(
    rb'https://www\.google\.com/maps/dir/\?api=1&destination=([^&]+)&travelmode=driving"'
)


def test_directions_link_uses_the_pins_own_coordinates_exactly():
    xml = build_pool_kml([place()], {"hanoi": [rec(lat=21.0301, lng=105.8712)]})

    coords = parse(xml).findall(".//k:Placemark/k:Point/k:coordinates", NS)[-1].text
    lng_str, lat_str, _ = coords.split(",")

    # The Places & Route layer's own anchor link comes first in document
    # order, so the pin's own link is the last match, not the first.
    matches = _DIRECTIONS_HREF_RE.findall(xml)
    assert matches, "no Directions link found in output"
    last_destination = matches[-1].decode()
    assert last_destination == f"{lat_str},{lng_str}"
    assert b"Directions" in xml


def test_pin_renders_coordinates_as_plain_text():
    desc = _description(rec(lat=21.0330476, lng=105.8462971), place())
    assert "Coords: 21.0330476, 105.8462971" in desc


def test_no_grab_link_anywhere_in_output():
    xml = build_pool_kml([place()], {"hanoi": [rec(lat=21.0301, lng=105.8712)]})
    assert b"grab://" not in xml


def test_description_omits_directions_and_coords_when_record_has_no_coordinates():
    r = rec()
    r.lat, r.lng = None, None
    desc = _description(r, place())
    assert "Directions" not in desc
    assert "Coords:" not in desc
    assert "grab://" not in desc


def test_description_includes_directions_link_and_coords_when_record_has_coordinates():
    desc = _description(rec(lat=21.0301, lng=105.8712), place())
    assert "Directions" in desc
    assert (
        "https://www.google.com/maps/dir/?api=1&destination=21.0301,105.8712"
        "&travelmode=driving" in desc
    )
    assert "Coords: 21.0301, 105.8712" in desc


def test_place_anchors_each_get_a_directions_link():
    places = [place("hanoi", "north"), place("hue", "central"), place("phu-quoc", "south")]
    xml = build_pool_kml(places, {})

    root_layer = parse(xml).findall(".//k:Folder", NS)[0]
    anchors = [
        p for p in root_layer.findall("k:Placemark", NS)
        if p.find("k:name", NS).text != "Route"
    ]
    assert len(anchors) == len(places)
    for anchor in anchors:
        desc = anchor.find("k:description", NS).text
        assert "Directions" in desc
        assert "https://www.google.com/maps/dir/?api=1" in desc
        assert "grab://" not in desc


def test_route_linestring_placemark_still_renders_neither():
    places = [place("hanoi", "north"), place("phu-quoc", "south")]
    xml = build_pool_kml(places, {})

    root_layer = parse(xml).findall(".//k:Folder", NS)[0]
    [route] = [
        p for p in root_layer.findall("k:Placemark", NS)
        if p.find("k:name", NS).text == "Route"
    ]
    assert route.find("k:description", NS) is None
    assert route.find("k:LineString", NS) is not None


def test_approximate_pins_still_get_a_directions_link_alongside_their_note():
    r = rec()
    r.location_precision = "approximate"
    desc = _description(r, place())

    assert "Approximate location" in desc
    assert "Directions" in desc
    assert desc.index("Approximate location") < desc.index("Directions"), (
        "the approximate-location note should read before the Directions action"
    )


# --- Per-station files (Task 11) --------------------------------------------


def test_place_kml_contains_only_that_places_records():
    hanoi, hue = place("hanoi", "north"), place("hue", "central")
    xml_hanoi = build_place_kml(hanoi, [rec(name="Hanoi Pho")])
    xml_hue = build_place_kml(hue, [rec(name="Hue Bun Bo")])

    assert "Hanoi Pho" in pin_names(xml_hanoi)
    assert "Hue Bun Bo" not in pin_names(xml_hanoi)
    assert "Hue Bun Bo" in pin_names(xml_hue)
    assert "Hanoi Pho" not in pin_names(xml_hue)


def test_place_kml_has_no_places_and_route_layer():
    xml = build_place_kml(place(), [rec()])
    assert "Places & Route" not in layer_names(xml)


def test_place_kml_first_layer_is_named_for_the_place_with_one_anchor_pin():
    p = place()
    xml = build_place_kml(p, [rec()])
    assert layer_names(xml)[0] == p.name

    first_folder = parse(xml).findall(".//k:Folder", NS)[0]
    placemarks = first_folder.findall("k:Placemark", NS)
    assert len(placemarks) == 1
    assert placemarks[0].find("k:name", NS).text == p.name
    assert placemarks[0].find("k:Point", NS) is not None
    assert placemarks[0].find("k:LineString", NS) is None


def test_place_kml_empty_category_produces_no_layer():
    xml = build_place_kml(place(), [rec("food")])
    assert layer_names(xml) == ["Hanoi", "Food"]


def test_place_kml_document_name_is_the_place_name():
    xml = build_place_kml(place(), [])
    doc_name = parse(xml).find(".//k:Document/k:name", NS).text
    assert doc_name == "Hanoi"


def test_place_kml_has_at_most_seven_layers():
    recs = [rec(c, f"r-{c}") for c in
            ("hotels", "must_see", "attractions", "food", "markets", "logistics")]
    assert len(layer_names(build_place_kml(place(), recs))) == 7


# --- Colour-coded links + YouTube video support (Task 12) ------------------
#
# The wider project has a fixed colour convention for link "actions"
# (documented across index.html): green = take me there, red = video. The
# KML must follow it. Directions turns green; attractions/must_see gain a
# red video link (the record's own video if set, else a YouTube search
# fallback that always resolves).


def test_directions_link_is_coloured_green():
    desc = _description(rec(lat=21.0301, lng=105.8712), place())
    assert '<a href="https://www.google.com/maps/dir/?api=1&destination=21.0301,105.8712&travelmode=driving" style="color:#0f7c5c;font-weight:700">Directions</a>' in desc


def test_attraction_with_video_renders_a_red_watch_link():
    r = rec(category="attractions", name="Ha Long Bay Cruise")
    r.video = "https://www.youtube.com/watch?v=abc123"
    desc = _description(r, place())
    assert (
        '<a href="https://www.youtube.com/watch?v=abc123" '
        'style="color:#cc0000;font-weight:700">Watch on YouTube</a>' in desc
    )


def test_attraction_without_video_renders_a_red_search_link():
    r = rec(category="attractions", name="Ha Long Bay Cruise")
    desc = _description(r, place())
    assert 'style="color:#cc0000;font-weight:700">Search YouTube</a>' in desc
    assert "https://www.youtube.com/results?search_query=" in desc
    # url-encoded query contains the record name and the place name
    assert "Ha+Long+Bay+Cruise" in desc
    assert "Hanoi" in desc


def test_must_see_record_gets_the_same_video_treatment():
    r = rec(category="must_see", name="Hoan Kiem Lake")
    desc = _description(r, place())
    assert 'style="color:#cc0000;font-weight:700">Search YouTube</a>' in desc

    r.video = "https://youtu.be/xyz789"
    desc = _description(r, place())
    assert (
        '<a href="https://youtu.be/xyz789" '
        'style="color:#cc0000;font-weight:700">Watch on YouTube</a>' in desc
    )


def test_hotel_record_gets_no_video_link_of_either_kind():
    desc = _description(rec("hotels", "Peridot"), place())
    assert "Watch on YouTube" not in desc
    assert "Search YouTube" not in desc
    assert "#cc0000" not in desc


def test_food_record_gets_no_video_link():
    desc = _description(rec("food", "Bun Cha"), place())
    assert "Watch on YouTube" not in desc
    assert "Search YouTube" not in desc
