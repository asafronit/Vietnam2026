"""Post-build checks. Nothing ships that fails these."""
import math

import lxml.etree as ET

from .inventory import Place, VIETNAM_LAT as LAT_RANGE, VIETNAM_LNG as LNG_RANGE
from .schema import Record

NS = {"k": "http://www.opengis.net/kml/2.2"}

# Hardened parser. lxml's default resolves entities and can fetch external
# DTDs, which makes XXE and billion-laughs possible. Today we only parse our
# own output, but a KML exported back out of My Maps is third-party input.
_PARSER = ET.XMLParser(resolve_entities=False, no_network=True, huge_tree=False)

MAX_LAYERS = 10
MAX_FEATURES_PER_LAYER = 2000
MAX_FEATURES_PER_MAP = 10000
MAX_BYTES = 5 * 1024 * 1024
EARTH_RADIUS_KM = 6371.0088


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def verify_kml(xml_bytes: bytes) -> list[str]:
    errors: list[str] = []

    if len(xml_bytes) > MAX_BYTES:
        errors.append(f"file is {len(xml_bytes) / 1048576:.1f}MB, over the 5MB limit")

    try:
        doc = ET.fromstring(xml_bytes, parser=_PARSER)
    except ET.XMLSyntaxError as exc:
        return errors + [f"not well-formed XML: {exc}"]

    folders = doc.findall(".//k:Folder", NS)
    if len(folders) > MAX_LAYERS:
        errors.append(f"{len(folders)} layers, max is {MAX_LAYERS}")

    for folder in folders:
        name_el = folder.find("k:name", NS)
        name = name_el.text if name_el is not None else "?"
        count = len(folder.findall("k:Placemark", NS))
        if count > MAX_FEATURES_PER_LAYER:
            errors.append(f"layer {name}: {count} features, max {MAX_FEATURES_PER_LAYER}")

    total = len(doc.findall(".//k:Placemark", NS))
    if total > MAX_FEATURES_PER_MAP:
        errors.append(f"{total} features, max {MAX_FEATURES_PER_MAP}")

    for el in doc.findall(".//k:Point/k:coordinates", NS):
        lng_s, lat_s = el.text.strip().split(",")[:2]
        lat, lng = float(lat_s), float(lng_s)
        if not (LAT_RANGE[0] <= lat <= LAT_RANGE[1]
                and LNG_RANGE[0] <= lng <= LNG_RANGE[1]):
            errors.append(f"coordinate {lat},{lng} is outside Vietnam")

    return errors


def verify_within_radius(
    places: list[Place], records: dict[str, list[Record]]
) -> list[str]:
    errors: list[str] = []
    for place in places:
        for rec in records.get(place.id, []):
            if rec.lat is None or rec.lng is None:
                continue
            distance = haversine_km(place.lat, place.lng, rec.lat, rec.lng)
            if distance > place.radius_km:
                errors.append(
                    f"{place.id}/{rec.name}: {distance:.0f} km from anchor, "
                    f"limit is {place.radius_km} km"
                )
    return errors
