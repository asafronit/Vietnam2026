"""Turn validated records into KML. Pure transform: no network, no disk."""
import lxml.etree as ET
from lxml.builder import ElementMaker

from .inventory import Place
from .schema import CATEGORIES, Record, is_shippable
from .style import (
    AVOID_COLOR,
    AVOID_ICON,
    HOTEL_TIER_SCALES,
    ICON_HREFS,
    PLACE_COLORS,
    hotel_style_id,
    style_id,
    to_kml_color,
)

KML_NS = "http://www.opengis.net/kml/2.2"
E = ElementMaker(namespace=KML_NS, nsmap={None: KML_NS})

CATEGORY_LABELS = {
    "hotels": "Hotels",
    "must_see": "Must-see",
    "attractions": "Attractions & Experiences",
    "food": "Food",
    "markets": "Markets & Shopping",
    "logistics": "Logistics",
}


def _directions_link(lat: float, lng: float) -> str:
    """Google Maps driving-directions URL for (lat, lng).

    Uses the documented Maps URLs API (`/maps/dir/?api=1&...`), which My Maps
    renders as a working link. A `grab://` deep link used to sit here, but My
    Maps strips custom URI schemes — it rendered as dead, unclickable text.
    No https form of the Grab deep link exists to fall back to, so the
    traveller's route to a Grab ride is the raw coordinates printed alongside
    this link (see `_location_lines`), copied by hand into the Grab app.
    lat/lng are interpolated the same way `<Point>` writes them, so the link
    and the pin always agree byte-for-byte.
    """
    return (
        "https://www.google.com/maps/dir/?api=1"
        f"&destination={lat},{lng}&travelmode=driving"
    )


def _location_lines(lat: float, lng: float) -> list[str]:
    """Directions link plus the raw coordinates as selectable plain text.

    The coordinates are not decorative: Grab cannot be deep-linked to from
    inside My Maps, so reading or copying them into the Grab app is the
    traveller's actual route to a ride. This is the degraded, JavaScript-free
    form of the clipboard-copy mechanism index.html implements for the same
    purpose.
    """
    return [
        f'<a href="{_directions_link(lat, lng)}">Directions</a>',
        f"Coords: {lat}, {lng}",
    ]


def _icon_style(style_ident: str, colour: str, scale: float, href: str):
    return E.Style(
        E.IconStyle(E.color(colour), E.scale(str(scale)), E.Icon(E.href(href))),
        id=style_ident,
    )


def _styles(places: list[Place]) -> list:
    out = []
    for place in places:
        colour = to_kml_color(PLACE_COLORS[place.id])

        for category in CATEGORIES:
            out.append(
                _icon_style(
                    style_id(place.id, category), colour, 1.1, ICON_HREFS[category]
                )
            )

        # Hotels get an extra style per star tier, plus one warning style.
        for tier, scale in HOTEL_TIER_SCALES.items():
            out.append(
                _icon_style(
                    hotel_style_id(place.id, tier, avoid=False),
                    colour,
                    scale,
                    ICON_HREFS["hotels"],
                )
            )
        out.append(
            _icon_style(
                hotel_style_id(place.id, 0, avoid=True),
                to_kml_color(AVOID_COLOR),
                1.1,
                AVOID_ICON,
            )
        )
    return out


def _description(rec: Record, place: Place) -> str:
    lines = [f"<b>{place.name}</b> &middot; {rec.area}"]

    if rec.location_precision == "approximate":
        lines.append("<i>Approximate location — search the name in Maps</i>")

    if rec.avoid:
        lines.append("<b>AVOID</b>")

    if rec.category == "hotels":
        stars = "star" if rec.tier == 1 else "stars"
        official = "" if rec.tier_official else " (self-declared)"
        lines.append(f"{rec.tier} {stars}{official}")
        price = f"${rec.price_low:.0f}"
        if rec.price_high and rec.price_high != rec.price_low:
            price += f"-${rec.price_high:.0f}"
        lines.append(f"{price}/night <i>(indicative, checked {rec.price_checked})</i>")
        if rec.price_high and rec.price_high > 200:
            lines.append("<i>upper room types exceed $200</i>")

    if rec.category == "food" and rec.signal:
        lines.append(rec.signal.replace("_", " "))

    # What it is, then why it is here. Both always present; the schema
    # guarantees neither is empty and that they say different things.
    lines.append(f"<br/>{rec.what}")
    lines.append(f"<b>Why it's here:</b> {rec.why}")

    links = " &middot; ".join(
        f'<a href="{url}">source {i}</a>' for i, url in enumerate(rec.sources, 1)
    )
    lines.append(links)

    if rec.lat is not None and rec.lng is not None:
        lines.extend(_location_lines(rec.lat, rec.lng))

    return "<br/>".join(lines)


def _placemark(rec: Record, place: Place):
    if rec.category == "hotels":
        ident = hotel_style_id(place.id, rec.tier or 3, rec.avoid)
    else:
        ident = style_id(place.id, rec.category)

    return E.Placemark(
        E.name(rec.name),
        E.styleUrl(f"#{ident}"),
        E.description(ET.CDATA(_description(rec, place))),
        E.Point(E.coordinates(f"{rec.lng},{rec.lat},0")),
    )


def _serialise(doc) -> bytes:
    return ET.tostring(
        E.kml(doc), xml_declaration=True, encoding="UTF-8", pretty_print=True
    )


def _anchor_placemark(place: Place):
    """A single place's own orientation pin: town centre, not a category pin."""
    description = (
        f"<b>{place.name}</b><br/>{place.region.title()}<br/>"
        + "<br/>".join(_location_lines(place.lat, place.lng))
    )
    return E.Placemark(
        E.name(place.name),
        E.styleUrl("#place-anchor"),
        E.description(ET.CDATA(description)),
        E.Point(E.coordinates(f"{place.lng},{place.lat},0")),
    )


def _places_layer(places: list[Place]):
    """Layer 1: the 14 anchors plus the locked route. The orientation layer.

    Pool-file only — a route spanning the whole country means nothing on a
    single-station map, so per-station files skip this layer entirely.
    """
    layer = E.Folder(E.name("Places & Route"))
    for place in places:
        layer.append(_anchor_placemark(place))
    path = " ".join(f"{p.lng},{p.lat},0" for p in places)
    layer.append(
        E.Placemark(
            E.name("Route"),
            E.styleUrl("#route"),
            E.LineString(E.coordinates(path)),
        )
    )
    return layer


def _anchor_layer(place: Place):
    """A per-station file's first layer: just that place's own anchor pin,
    named after the place so the traveller can see the town centre without
    the country-spanning route that would mean nothing on a single stop."""
    layer = E.Folder(E.name(place.name))
    layer.append(_anchor_placemark(place))
    return layer


def _place_anchor_style():
    return _icon_style(
        "place-anchor", to_kml_color("#42276f"), 1.2,
        "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png",
    )


def _category_layers(
    place_records: list[tuple[Place, list[Record]]]
) -> list:
    """One Folder per category that has at least one shippable record, in
    CATEGORIES order. Shared between the pool file (many places) and each
    per-station file (one place), so filtering only lives here once."""
    layers = []
    for category in CATEGORIES:
        layer = E.Folder(E.name(CATEGORY_LABELS[category]))
        count = 0
        for place, records in place_records:
            for rec in records:
                if rec.category != category or not is_shippable(rec):
                    continue
                layer.append(_placemark(rec, place))
                count += 1
        if count:
            layers.append(layer)
    return layers


def build_pool_kml(
    places: list[Place], records: dict[str, list[Record]]
) -> bytes:
    """One document, seven layers, all 14 places. My Maps has no hierarchy
    beyond map -> layer -> feature, so this is deliberately flat."""
    doc = E.Document(E.name("Vietnam 2026 - Pool"))

    for style in _styles(places):
        doc.append(style)
    doc.append(
        E.Style(E.LineStyle(E.color(to_kml_color("#42276f")), E.width("4")), id="route")
    )
    doc.append(_place_anchor_style())

    doc.append(_places_layer(places))

    for layer in _category_layers([(place, records.get(place.id, [])) for place in places]):
        doc.append(layer)

    return _serialise(doc)


def build_place_kml(place: Place, records: list[Record]) -> bytes:
    """One station's own file: up to six category layers plus a single
    anchor layer for that place, never the whole-country route. Shares
    description, styling and filtering with the pool build so the two never
    drift apart."""
    doc = E.Document(E.name(place.name))

    for style in _styles([place]):
        doc.append(style)
    doc.append(_place_anchor_style())

    doc.append(_anchor_layer(place))

    for layer in _category_layers([(place, records)]):
        doc.append(layer)

    return _serialise(doc)
