"""Inter-city transfers: the ways to get from one station to another.

A transfer is deliberately not a `Record`. A record is a place with a pin; a
transfer joins two places and carries several competing ways to make the trip
-- a night train, a sleeper bus, a private car -- each with its own boarding
point, timetable and price. Folding it into a POI category would put it in the
station counts, on the map and in search, none of which it belongs to.

One YAML file per pair, `data/transfers/<from>__<to>.yaml`, so that pairs can
be researched in parallel without edit conflicts.
"""
import glob
import os
import re
from dataclasses import dataclass, field, fields

import yaml

from .inventory import VIETNAM_LAT, VIETNAM_LNG

MODES = (
    "flight",
    "train",
    "sleeper_train",
    "sleeper_bus",
    "limousine_van",
    "bus",
    "private_car",
    "boat",
    "speedboat",
    # Two legs sold or taken as one: the night train to Lao Cai plus the
    # shuttle up to Sapa, the bus to Ha Tien plus the speedboat to Phu Quoc.
    "combo",
)
# Prices stay in the currency they were quoted in. The site already holds the
# fixed exchange rates; converting here as well would make two sources of truth.
CURRENCIES = ("VND", "USD")
# A private car is priced per vehicle and a sleeper cabin per cabin -- reading
# either as per person would make it look four times as expensive.
TRANSFER_PRICE_UNITS = ("per_person", "per_vehicle", "per_cabin")
CONFIDENCE_LEVELS = ("high", "medium", "low")
# The language an operator's name is written in. It becomes the lang attribute
# on the page, so a Hebrew screen reader voices "Hung Thanh" with Vietnamese
# phonemes instead of Hebrew ones. Declared per option, never guessed.
OP_LANGS = ("vi", "en")

_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Asaf's standing rule (memory: feedback_avoid_vietjet): Vietjet is never
# priced or offered. Enforced here so a research pass can't slip it back in.
_BANNED_OPERATOR_RE = re.compile(r"viet\s*jet", re.IGNORECASE)


@dataclass
class Stop:
    name: str
    # Latin script: it is what you show the driver.
    address: str = ""
    # True when the operator collects you from your hotel. The address may
    # then describe the pickup area, and no coordinates are needed because
    # there is nowhere to ride to.
    pickup_hotel: bool = False
    # Required for a boarding point the traveller must reach: they feed the
    # Grab button (grab:// drop_off_lat/lng, plus the address to paste).
    lat: float | None = None
    lng: float | None = None
    # השפה שבה הכתובת ושם נקודת העלייה כתובים, בדיוק כמו op_lang למפעיל.
    # ברירת המחדל en ולא vi, וזו החלטה מכוונת: המחרוזות האלה הן ברובן
    # אנגלית עם שם מקום ויאטנמי בתוכה — "Dak Lak bus company yard (route
    # 12 terminus)", "Tan Son Nhat Airport, Terminal T3 (domestic)" — ולכן
    # תג vi גורף היה מצווה על קורא מסך עברי להגות משפט אנגלי שלם בפונמות
    # ויאטנמיות. תג en על טוקן ויאטנמי בודד הוא פגיעה קטנה בהרבה.
    lang: str = "en"


@dataclass
class TransferOption:
    mode: str
    operator: str
    board: Stop | None
    confidence: str
    alight: Stop | None = None
    departures: str = ""
    departures_he: str | None = None
    op_lang: str = "en"
    duration_min: int | None = None
    duration_max: int | None = None
    price_low: float | None = None
    price_high: float | None = None
    currency: str | None = None
    price_unit: str | None = None
    # One link per company that sells the trip -- a flight route is flown by
    # several airlines, and each gets its own button. [{name, url}, ...]
    book_links: list[dict] = field(default_factory=list)
    pros: list[str] = field(default_factory=list)
    pros_he: list[str] | None = None
    cons: list[str] = field(default_factory=list)
    cons_he: list[str] | None = None
    tips: str | None = None
    tips_he: str | None = None
    sources: list[str] = field(default_factory=list)
    # Per option, not per transfer: a train fare and a van fare are checked
    # on different days.
    checked: str | None = None


@dataclass
class Transfer:
    origin: str
    destination: str
    options: list[TransferOption]
    # The page may offer the pair in the opposite direction too, flagged as
    # such. Doubles coverage without doubling the research.
    reverse_ok: bool = False
    note: str | None = None
    note_he: str | None = None
    source_file: str = ""

    @property
    def label(self) -> str:
        return f"transfers/{self.origin}__{self.destination}"


_TRANSFER_KEYS = {"from", "to", "reverse_ok", "note", "note_he", "options"}


def _read_yaml(path: str) -> tuple[dict | None, str | None]:
    """Parse one transfer file. A syntax error comes back as a message, not a raise,
    so a stray colon in a Hebrew sentence reads as INVALID instead of a traceback."""
    with open(path, encoding="utf-8") as fh:
        try:
            return (yaml.safe_load(fh) or {}), None
        except yaml.YAMLError as exc:
            mark = getattr(exc, "problem_mark", None)
            where = f" at line {mark.line + 1}, column {mark.column + 1}" if mark else ""
            problem = getattr(exc, "problem", None) or str(exc)
            return None, f"YAML syntax error{where}: {problem}"


def _known(cls) -> set[str]:
    return {f.name for f in fields(cls)}


def _stop(raw) -> Stop | None:
    if raw is None:
        return None
    raw = dict(raw)
    return Stop(
        name=str(raw.get("name", "")),
        address=str(raw.get("address", "") or ""),
        pickup_hotel=bool(raw.get("pickup_hotel", False)),
        lat=raw.get("lat"),
        lng=raw.get("lng"),
        lang=str(raw.get("lang", "en") or "en"),
    )


def _option(raw: dict) -> TransferOption:
    # Unknown keys are dropped here and reported by `check_transfer_keys`, so
    # a typo surfaces as an INVALID line instead of a TypeError traceback.
    raw = {k: v for k, v in dict(raw).items() if k in _known(TransferOption)}
    board = _stop(raw.pop("board", None))
    alight = _stop(raw.pop("alight", None))
    # YAML reads an unquoted 2026-10-06 as a date; the contract is a string.
    if raw.get("checked") is not None:
        raw["checked"] = str(raw["checked"])
    return TransferOption(board=board, alight=alight, **raw)


def load_transfers(directory: str) -> list[Transfer]:
    """Every transfer under `directory`, in filename order. A missing directory is []."""
    if not os.path.isdir(directory):
        return []
    transfers: list[Transfer] = []
    for path in sorted(glob.glob(os.path.join(directory, "*.yaml"))):
        raw, error = _read_yaml(path)
        if error is not None:
            continue  # reported by check_transfer_keys
        transfers.append(
            Transfer(
                origin=str(raw.get("from", "")),
                destination=str(raw.get("to", "")),
                options=[_option(o) for o in raw.get("options") or []],
                reverse_ok=bool(raw.get("reverse_ok", False)),
                note=raw.get("note"),
                note_he=raw.get("note_he"),
                source_file=os.path.basename(path),
            )
        )
    return transfers


def check_transfer_keys(directory: str) -> list[str]:
    """Every key the model does not know, by file and level.

    Hand-written YAML is where typos live: `prise_low` would otherwise be
    silently ignored (and the option then fail for a missing price, with a
    message pointing at the wrong thing) or crash the loader outright.
    """
    if not os.path.isdir(directory):
        return []
    errors: list[str] = []
    option_keys = _known(TransferOption)
    stop_keys = _known(Stop)
    for path in sorted(glob.glob(os.path.join(directory, "*.yaml"))):
        name = os.path.basename(path)
        raw, error = _read_yaml(path)
        if error is not None:
            errors.append(f"transfers/{name}: {error}")
            continue
        for key in sorted(set(raw) - _TRANSFER_KEYS):
            errors.append(f"transfers/{name}: unknown key {key!r}")
        for i, opt in enumerate(raw.get("options") or []):
            for key in sorted(set(opt) - option_keys):
                errors.append(f"transfers/{name}/option[{i}]: unknown key {key!r}")
            for stop_name in ("board", "alight"):
                stop = opt.get(stop_name)
                if isinstance(stop, dict):
                    for key in sorted(set(stop) - stop_keys):
                        errors.append(
                            f"transfers/{name}/option[{i}]/{stop_name}: unknown key {key!r}"
                        )
    return errors


def _in_vietnam(lat, lng) -> tuple[bool, bool]:
    lat_ok = isinstance(lat, (int, float)) and VIETNAM_LAT[0] <= lat <= VIETNAM_LAT[1]
    lng_ok = isinstance(lng, (int, float)) and VIETNAM_LNG[0] <= lng <= VIETNAM_LNG[1]
    return lat_ok, lng_ok


def _validate_board(where: str, board: Stop | None) -> list[str]:
    if board is None:
        return [f"{where}: board is required"]
    errors: list[str] = []
    if not board.name.strip():
        errors.append(f"{where}: board.name is empty")
    if board.lang not in OP_LANGS:
        errors.append(f"{where}: board.lang must be one of {OP_LANGS}")
    if not board.pickup_hotel:
        if not board.address.strip():
            errors.append(f"{where}: board.address is empty (or set pickup_hotel: true)")
        # Without coordinates there is no Grab button, and reaching the
        # boarding point is the whole reason the address is here.
        if board.lat is None or board.lng is None:
            errors.append(f"{where}: board.lat/lng required for the Grab link")
        else:
            lat_ok, lng_ok = _in_vietnam(board.lat, board.lng)
            if not lat_ok:
                errors.append(f"{where}: board.lat {board.lat} is outside Vietnam")
            if not lng_ok:
                errors.append(f"{where}: board.lng {board.lng} is outside Vietnam")
    return errors


def _validate_hebrew_list(where: str, name: str, english: list[str], hebrew) -> list[str]:
    if hebrew is None:
        return [f"{where}: {name} is required"]
    if len(hebrew) != len(english) or any(not str(h).strip() for h in hebrew):
        return [f"{where}: {name} must match {name[:-3]} item for item"]
    return []


def _validate_option(where: str, opt: TransferOption) -> list[str]:
    errors: list[str] = []
    if opt.mode not in MODES:
        errors.append(f"{where}: mode must be one of {MODES}")
    if not (opt.operator or "").strip():
        errors.append(f"{where}: operator is empty")
    if opt.op_lang not in OP_LANGS:
        errors.append(f"{where}: op_lang must be one of {OP_LANGS}")
    if opt.confidence not in CONFIDENCE_LEVELS:
        errors.append(f"{where}: confidence must be one of {CONFIDENCE_LEVELS}")

    errors.extend(_validate_board(where, opt.board))

    if opt.duration_min is None:
        errors.append(f"{where}: duration_min is required")
    elif opt.duration_max is not None and opt.duration_max < opt.duration_min:
        errors.append(f"{where}: duration_max {opt.duration_max} below duration_min {opt.duration_min}")

    if opt.price_low is None:
        errors.append(f"{where}: price_low is required")
    elif opt.price_high is not None and opt.price_high < opt.price_low:
        errors.append(f"{where}: price_high {opt.price_high} below price_low {opt.price_low}")
    if opt.currency not in CURRENCIES:
        errors.append(f"{where}: currency must be one of {CURRENCIES}")
    if opt.price_unit not in TRANSFER_PRICE_UNITS:
        errors.append(f"{where}: price_unit must be one of {TRANSFER_PRICE_UNITS}")

    for j, link in enumerate(opt.book_links):
        if not str(link.get("name", "")).strip():
            errors.append(f"{where}: book_links[{j}] needs a name")
        if not str(link.get("url", "")).startswith("https://"):
            errors.append(f"{where}: book_links[{j}] url must start with https://")

    banned = [opt.operator or ""] + [
        f"{l.get('name', '')} {l.get('url', '')}" for l in opt.book_links
    ]
    if any(_BANNED_OPERATOR_RE.search(text) for text in banned):
        errors.append(f"{where}: Vietjet is excluded from this guide (operator or book_links)")

    if not opt.sources:
        errors.append(f"{where}: needs at least one source")
    if not opt.checked or not _ISO_DATE_RE.match(opt.checked):
        errors.append(f"{where}: checked must be an ISO date (YYYY-MM-DD)")

    errors.extend(_validate_hebrew_list(where, "pros_he", opt.pros, opt.pros_he))
    errors.extend(_validate_hebrew_list(where, "cons_he", opt.cons, opt.cons_he))
    if (opt.departures or "").strip() and not (opt.departures_he or "").strip():
        errors.append(f"{where}: departures needs departures_he")
    if (opt.tips or "").strip() and not (opt.tips_he or "").strip():
        errors.append(f"{where}: tips needs tips_he")
    return errors


def validate_transfers(transfers: list[Transfer], place_ids: set[str]) -> list[str]:
    errors: list[str] = []
    seen: dict[tuple[str, str], str] = {}
    for t in transfers:
        where = t.label
        if t.origin not in place_ids:
            errors.append(f"{where}: from {t.origin!r} is not a station id")
        if t.destination not in place_ids:
            errors.append(f"{where}: to {t.destination!r} is not a station id")
        if t.origin == t.destination:
            errors.append(f"{where}: from and to are the same station")
        pair = (t.origin, t.destination)
        if pair in seen:
            errors.append(f"{where}: duplicate pair, also in {seen[pair]} ({t.source_file})")
        else:
            seen[pair] = t.source_file
        if not t.options:
            errors.append(f"{where}: needs at least one option")
        if (t.note or "").strip() and not (t.note_he or "").strip():
            errors.append(f"{where}: note needs note_he")
        for i, opt in enumerate(t.options):
            errors.extend(_validate_option(f"{where}/option[{i}]", opt))
    return errors


def _stop_to_web_json(stop: Stop | None) -> dict | None:
    if stop is None:
        return None
    return {
        "name": stop.name,
        "address": stop.address,
        "pickupHotel": stop.pickup_hotel,
        "lat": stop.lat,
        "lng": stop.lng,
        "lang": stop.lang,
    }


def _option_to_web_json(opt: TransferOption) -> dict:
    """Explicit field list, as in `_record_to_web_json`: a future model field
    must never reach the page by accident. Every key is always present (null
    when unset) so the page never tests for existence."""
    return {
        "mode": opt.mode,
        "operator": opt.operator,
        "opLang": opt.op_lang,
        "board": _stop_to_web_json(opt.board),
        "alight": _stop_to_web_json(opt.alight),
        "departures": opt.departures,
        "departuresHe": opt.departures_he,
        "durationMin": opt.duration_min,
        "durationMax": opt.duration_max,
        "priceLow": opt.price_low,
        "priceHigh": opt.price_high,
        "currency": opt.currency,
        "priceUnit": opt.price_unit,
        "bookLinks": [{"name": l["name"], "url": l["url"]} for l in opt.book_links],
        "pros": opt.pros,
        "prosHe": opt.pros_he,
        "cons": opt.cons,
        "consHe": opt.cons_he,
        "tips": opt.tips,
        "tipsHe": opt.tips_he,
        "sources": opt.sources,
        "checked": opt.checked,
        "confidence": opt.confidence,
    }


def transfer_to_web_json(t: Transfer) -> dict | None:
    """Low-confidence options never ship; a transfer left with none is dropped."""
    options = [_option_to_web_json(o) for o in t.options if o.confidence != "low"]
    if not options:
        return None
    return {
        "from": t.origin,
        "to": t.destination,
        "reverseOk": t.reverse_ok,
        "note": t.note,
        "noteHe": t.note_he,
        "options": options,
    }
