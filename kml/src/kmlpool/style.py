"""Colour and icon mapping.

KML colours are aabbggrr, not rrggbb. Getting this backwards is the classic
KML bug: it silently swaps red and blue and nothing errors.
"""

PLACE_COLORS: dict[str, str] = {
    "hanoi":         "#e6194b",
    "ha-giang":      "#f58231",
    "sapa":          "#ffe119",
    "ha-long":       "#3cb44b",
    "ninh-binh":     "#42d4f4",
    "phong-nha":     "#4363d8",
    "hue":           "#911eb4",
    "hoi-an":        "#f032e6",
    "buon-ma-thuot": "#9a6324",
    "lak-lake":      "#808000",
    "da-lat":        "#469990",
    "saigon":        "#000075",
    "mekong":        "#800000",
    "phu-quoc":      "#a9a9a9",
}

_SHAPES = "http://maps.google.com/mapfiles/kml/shapes"

ICON_HREFS: dict[str, str] = {
    "hotels":      f"{_SHAPES}/lodging.png",
    "must_see":    f"{_SHAPES}/star.png",
    "attractions": f"{_SHAPES}/hiker.png",
    "food":        f"{_SHAPES}/dining.png",
    # street_food and restaurants split out of `food`. My Maps offers no
    # separate street-stall icon, so the two share the dining pin and are
    # told apart by their layer, not their glyph.
    "street_food": f"{_SHAPES}/dining.png",
    "restaurants": f"{_SHAPES}/dining.png",
    "markets":     f"{_SHAPES}/shopping.png",
    "nightlife":   f"{_SHAPES}/bars.png",
    "spa":         f"{_SHAPES}/parks.png",
    "logistics":   f"{_SHAPES}/airports.png",
    # Contacts never reach the KML — a person has no coordinates, so the
    # record is never shippable and the layer is dropped as empty. The entry
    # exists because styles are emitted per category before that test runs,
    # and because a category without an icon is a gap the style test refuses.
    "contacts":    f"{_SHAPES}/phone.png",
}


# Hotels carry a second visual axis on top of place colour: pin size encodes
# star tier, and a hotel flagged `avoid` turns red with a caution icon so a
# known-bad option cannot be picked by accident at midnight.
HOTEL_TIER_SCALES: dict[int, float] = {5: 1.4, 4: 1.1, 3: 0.9}
# Must stay distinct from every place colour in PLACE_COLORS, or an avoided
# hotel in that place is indistinguishable from the place's own anchor pin.
AVOID_COLOR = "#d7263d"
AVOID_ICON = f"{_SHAPES}/caution.png"


def hotel_style_id(place_id: str, tier: int, avoid: bool) -> str:
    if avoid:
        return f"s-{place_id}-hotels-avoid"
    return f"s-{place_id}-hotels-t{tier}"


def to_kml_color(hex_rgb: str, alpha: str = "ff") -> str:
    """Convert #rrggbb to KML's aabbggrr byte order."""
    value = hex_rgb.lstrip("#")
    if len(value) != 6:
        raise ValueError(f"expected 6 hex digits, got {hex_rgb!r}")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(f"not valid hex: {hex_rgb!r}") from exc
    rr, gg, bb = value[0:2], value[2:4], value[4:6]
    return f"{alpha}{bb}{gg}{rr}"


def style_id(place_id: str, category: str) -> str:
    return f"s-{place_id}-{category}"
