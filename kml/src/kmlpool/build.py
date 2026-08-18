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


def _grab_link(lat: float, lng: float) -> str:
    """Grab deep link for a drop-off at (lat, lng).

    Mirrors the established convention in index.html — same href shape, same
    query params. My Maps strips JavaScript from descriptions, so unlike the
    site's grab-link anchors this carries only the href: no web fallback, no
    clipboard copy. lat/lng are interpolated the same way `<Point>` writes
    them, so the two always agree byte-for-byte.
    """
    return f"grab://open?screenType=BOOKING&drop_off_lat={lat}&drop_off_lng={lng}"


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
        lines.append(f'<a href="{_grab_link(rec.lat, rec.lng)}">Grab ride here</a>')

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


def _places_layer(places: list[Place]):
    """Layer 1: the 14 anchors plus the locked route. The orientation layer."""
    layer = E.Folder(E.name("Places & Route"))
    for place in places:
        description = (
            f"<b>{place.name}</b><br/>{place.region.title()}"
            f'<br/><a href="{_grab_link(place.lat, place.lng)}">Grab ride here</a>'
        )
        layer.append(
            E.Placemark(
                E.name(place.name),
                E.styleUrl("#place-anchor"),
                E.description(ET.CDATA(description)),
                E.Point(E.coordinates(f"{place.lng},{place.lat},0")),
            )
        )
    path = " ".join(f"{p.lng},{p.lat},0" for p in places)
    layer.append(
        E.Placemark(
            E.name("Route"),
            E.styleUrl("#route"),
            E.LineString(E.coordinates(path)),
        )
    )
    return layer


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
    doc.append(
        _icon_style(
            "place-anchor", to_kml_color("#42276f"), 1.2,
            "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png",
        )
    )

    doc.append(_places_layer(places))

    for category in CATEGORIES:
        layer = E.Folder(E.name(CATEGORY_LABELS[category]))
        count = 0
        for place in places:
            for rec in records.get(place.id, []):
                if rec.category != category or not is_shippable(rec):
                    continue
                layer.append(_placemark(rec, place))
                count += 1
        if count:
            doc.append(layer)

    return _serialise(doc)
