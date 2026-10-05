"""Record model plus the validation rules the spec's misinformation controls require."""
import re
from dataclasses import dataclass, field

# `food` נשאר כדי לא לשבור את הקבצים הקיימים, אבל רשומות חדשות נכתבות
# ל-street_food או ל-restaurants. הפיצול נדרש כי דוכן ברחוב ומסעדת מישלין
# הם החלטות שונות לגמרי למטייל, ובעיקר: הם נפגעים מגשם בצורה שונה.
CATEGORIES = (
    "hotels",
    "must_see",
    "attractions",
    "food",
    "street_food",
    "restaurants",
    "markets",
    "nightlife",
    "spa",
    # Diving is split out of `attractions` rather than left inside it because
    # the decisions are different in kind: a dive site is chosen by depth and
    # certification, a club by affiliation and group size, and the whole
    # activity is governed by a sea state that closes it for months at a
    # time. Cham Island is the proof -- it sat in `attractions` reading like
    # a day trip you could book any time, and it is shut for half the year.
    "diving",
    "logistics",
    # People rather than places: the agent who booked the trip, the dive club,
    # the fixer who handles the visa. They belong in a field guide for the same
    # reason a phone number belongs in a wallet, and the website already had
    # the category, the label and the purple WhatsApp button waiting for them.
    "contacts",
)

# עד כמה כל סוג פעילות נפגע מגשם. נקרא ע"י האתר לחישוב ההיתכנות,
# ונשמר כאן כדי שמקור האמת יהיה אחד.
WEATHER_SENSITIVITY = {
    "must_see": "medium",
    "attractions": "high",
    "markets": "medium",
    "street_food": "medium",
    "food": "medium",
    "restaurants": "low",
    "hotels": "low",
    "nightlife": "low",
    "spa": "low",
    # The most weather-bound category in the pool. Not just rain: wind drives
    # the swell, swell kills visibility, and an operator cancels the day.
    "diving": "high",
    "logistics": "medium",
    "contacts": "low",
}
SENSITIVITY_LEVELS = ("high", "medium", "low")

# What the price buys. Without this a bare number is unreadable: 15 dollars
# is cheap for a hotel night, ordinary for a dive, and absurd for a bowl of pho.
PRICE_UNITS = ("per_night", "per_person", "per_dish", "entry", "per_hour", "free")
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
    # Defaulted so a placeless record -- a dish, a person -- can omit it
    # entirely in YAML. The requirement has not moved: validate_record still
    # rejects an empty query for every category that describes a place.
    geocode_query: str = ""
    sources: list[str] = field(default_factory=list)
    # Hebrew content. `name` deliberately stays in Latin script -- it is what
    # you show a taxi driver -- but everything a reader reads gets a Hebrew
    # twin. Missing values fall back to the English text at render time.
    what_he: str | None = None
    why_he: str | None = None
    area_he: str | None = None
    name_he: str | None = None      # transliteration, only where it helps
    # Cost. Previously hotels-only; now any record may carry one, because
    # "how much is this going to cost me" is the question every category
    # raises. USD, and `price_unit` says what the number buys.
    price_low: float | None = None
    price_high: float | None = None
    price_checked: str | None = None
    price_unit: str | None = None   # per_night, per_person, per_dish, entry, free
    # hotels only
    tier: int | None = None
    tier_official: bool | None = None
    avoid: bool = False          # known-bad; renders red with a caution icon
    # food / street_food / restaurants only
    kind: str | None = None          # cuisine: vietnamese, international
    signal: str | None = None
    # A dish or product rather than a venue -- banh cuon, thang co, artichoke
    # tea. These have no address, so geocoding them is meaningless: the query
    # either misses or drifts to a city centre, and the pin then lies. Marked
    # records skip the geocoder entirely and stay out of the review queue.
    # Deliberately NOT folded into `kind`, which already means cuisine and is
    # still `vietnamese` for every one of these.
    is_dish: bool = False
    # Ways to reach a person. `whatsapp` is digits with or without punctuation;
    # the website strips everything but digits for the wa.me URL and renders it
    # as the purple action the link convention reserves for a human contact.
    whatsapp: str | None = None
    phone: str | None = None
    email: str | None = None
    # דריסה ידנית של רגישות מזג האוויר, כשברירת המחדל של הקטגוריה שגויה
    # (מערה בקטגוריית attractions, שוק מקורה בקטגוריית markets).
    weather: str | None = None
    # attractions/must_see only (optional): a YouTube URL rendered as a
    # "Watch on YouTube" link. Not required, and not enforced as required
    # for those categories — a missing value falls back to a search link.
    video: str | None = None
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
    # A dish has no address, and neither does a person: geocoding either one
    # produces a pin in a city centre that lies about where the thing is.
    # Both skip the geocoder and stay out of the review queue.
    _placeless = rec.is_dish or rec.category == "contacts"
    if not _placeless and not rec.geocode_query.strip():
        errors.append(f"{where}: geocode_query is empty")
    if rec.is_dish and rec.category not in ("food", "street_food", "restaurants"):
        errors.append(f"{where}: is_dish only applies to food categories")
    if rec.confidence not in CONFIDENCE_LEVELS:
        errors.append(f"{where}: confidence must be one of {CONFIDENCE_LEVELS}")

    # A contact nobody can reach is not a contact. The whole point of the
    # category is the tap that opens WhatsApp, the dialler or the mail app.
    if rec.category == "contacts" and not (rec.whatsapp or rec.phone or rec.email):
        errors.append(f"{where}: a contact needs a whatsapp, phone or email")

    if rec.weather is not None and rec.weather not in SENSITIVITY_LEVELS:
        errors.append(f"{where}: weather must be one of {SENSITIVITY_LEVELS}")

    if rec.price_unit is not None and rec.price_unit not in PRICE_UNITS:
        errors.append(f"{where}: price_unit must be one of {PRICE_UNITS}")
    # A number with no unit is a number nobody can act on.
    if rec.price_low is not None and rec.price_unit is None:
        errors.append(f"{where}: price_low needs a price_unit")
    if rec.price_high is not None and rec.price_low is None:
        errors.append(f"{where}: price_high without price_low")
    if (
        rec.price_low is not None
        and rec.price_high is not None
        and rec.price_high < rec.price_low
    ):
        errors.append(f"{where}: price_high {rec.price_high} below price_low {rec.price_low}")

    if rec.video is not None:
        if not rec.video.startswith("https://") or not any(
            domain in rec.video for domain in ("youtube.com", "youtu.be")
        ):
            errors.append(f"{where}: video must be a https:// youtube.com or youtu.be URL")

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


def validate_hebrew(
    place_id: str, records: list[Record], declared_complete: bool
) -> list[str]:
    """Enforce Hebrew coverage, but only where a place claims to have it.

    A blanket rule would be useless here: most places carry no Hebrew yet, so
    requiring it everywhere would fail the build on every one of them and block
    the very work that fills the gap. Instead each place declares
    `hebrew_complete: true` in its YAML once it has been translated, and from
    that moment the claim is enforced -- so a later edit that adds an untranslated
    record to a finished place fails loudly instead of quietly reopening a hole.

    `name_he` and `area_he` are deliberately not required. The site falls back to
    the Latin name when no transliteration exists, which is the wanted behaviour:
    the Latin name is what you show a taxi driver.
    """
    if not declared_complete:
        return []

    errors: list[str] = []
    for rec in records:
        # Records the web pool would drop anyway cannot leave a visible hole.
        if not is_web_shippable(rec):
            continue
        missing = [
            field
            for field, value in (("what_he", rec.what_he), ("why_he", rec.why_he))
            if not (value or "").strip()
        ]
        if missing:
            errors.append(
                f"{place_id}/{rec.category}/{rec.name}: declared hebrew_complete "
                f"but missing {', '.join(missing)}"
            )
    return errors


def is_shippable(rec: Record) -> bool:
    """Low-confidence records and ungeocoded records never reach the KML."""
    if rec.confidence == "low":
        return False
    if rec.lat is None or rec.lng is None:
        return False
    return not validate_record(rec)


def is_web_shippable(rec: Record) -> bool:
    """The web pool's gate. Deliberately looser than `is_shippable`.

    KML is a map format, so a pin without coordinates is meaningless there.
    A web card is not: it can show the name, the description and the reason,
    and link out to a maps *search* instead of a fixed point. Requiring
    coordinates for the website was inherited from the KML path by accident,
    and it was silently withholding roughly half the researched records from
    the site. Confidence and validity still gate; geocoding no longer does.
    """
    if rec.confidence == "low":
        return False
    return not validate_record(rec)
