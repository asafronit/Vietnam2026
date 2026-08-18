"""Record model plus the validation rules the spec's misinformation controls require."""
import re
from dataclasses import dataclass, field

CATEGORIES = ("hotels", "must_see", "attractions", "food", "markets", "logistics")
CONFIDENCE_LEVELS = ("high", "medium", "low")
PRICE_CAP_USD = 200.0
MAX_HOTELS_PER_TIER = 2
HOTEL_TIERS = (5, 4, 3)


@dataclass
class Record:
    name: str
    category: str
    area: str
    what: str      # what this place is, for someone who has never heard of it
    why: str       # why it earned a place in the pool
    confidence: str
    geocode_query: str
    sources: list[str] = field(default_factory=list)
    # hotels only
    tier: int | None = None
    tier_official: bool | None = None
    price_low: float | None = None
    price_high: float | None = None
    price_checked: str | None = None
    avoid: bool = False          # known-bad; renders red with a caution icon
    # food only
    kind: str | None = None
    signal: str | None = None
    # filled by the geocode stage
    lat: float | None = None
    lng: float | None = None
    # "approximate" when lat/lng came from a fallback rung rather than the
    # exact geocode_query; None (omitted from YAML) for an exact hit.
    location_precision: str | None = None


# Trailing punctuation stripped before the what/why sameness check, so a
# stray period or ellipsis doesn't let a byte-identical restatement slip
# through. Deliberately narrow: normalised *equality* only, not similarity.
_TRAILING_PUNCTUATION_RE = re.compile(r"[\s.!…?]+$")


def _normalized_for_sameness_check(text: str) -> str:
    """Casefold, strip surrounding whitespace, and strip trailing punctuation.

    Used only to catch a `why` that restates `what` verbatim modulo case,
    whitespace or a trailing full stop/ellipsis. Not a paraphrase detector:
    genuinely different wording is left alone by design.
    """
    return _TRAILING_PUNCTUATION_RE.sub("", text.strip()).casefold()


def validate_record(rec: Record) -> list[str]:
    errors: list[str] = []
    where = f"{rec.category}/{rec.name}"

    if rec.category not in CATEGORIES:
        errors.append(f"{where}: unknown category {rec.category}")
    if not rec.name.strip():
        errors.append(f"{where}: name is empty")
    if not rec.what.strip():
        errors.append(f"{where}: what is empty")
    if not rec.why.strip():
        errors.append(f"{where}: why is empty")
    if rec.what.strip() and _normalized_for_sameness_check(rec.what) == _normalized_for_sameness_check(rec.why):
        errors.append(f"{where}: why must not restate what")
    if not rec.area.strip():
        errors.append(f"{where}: area is empty")
    if not rec.geocode_query.strip():
        errors.append(f"{where}: geocode_query is empty")
    if rec.confidence not in CONFIDENCE_LEVELS:
        errors.append(f"{where}: confidence must be one of {CONFIDENCE_LEVELS}")

    required_sources = 2 if rec.category == "hotels" else 1
    if len(rec.sources) < required_sources:
        if required_sources == 2:
            errors.append(f"{where}: hotels need at least two sources")
        else:
            errors.append(f"{where}: needs at least one source")

    if rec.category == "hotels":
        if rec.tier not in HOTEL_TIERS:
            errors.append(f"{where}: tier must be 5, 4 or 3")
        if rec.price_low is None:
            errors.append(f"{where}: price_low is required")
        elif rec.price_low > PRICE_CAP_USD:
            errors.append(
                f"{where}: price_low {rec.price_low} exceeds the 200 USD cap"
            )
        if not rec.price_checked:
            errors.append(f"{where}: price_checked date is required")

    return errors


def validate_hotels(place_id: str, hotels: list[Record]) -> list[str]:
    errors: list[str] = []
    for tier in HOTEL_TIERS:
        count = sum(1 for h in hotels if h.tier == tier)
        if count > MAX_HOTELS_PER_TIER:
            errors.append(
                f"{place_id}: {count} hotels in tier {tier}, max is {MAX_HOTELS_PER_TIER}"
            )
    return errors


def is_shippable(rec: Record) -> bool:
    """Low-confidence records and ungeocoded records never reach the KML."""
    if rec.confidence == "low":
        return False
    if rec.lat is None or rec.lng is None:
        return False
    return not validate_record(rec)
