import json

from kmlpool.geocode import Geocoder, write_review_queue
from kmlpool.inventory import Place
from kmlpool.schema import Record

HANOI = Place("hanoi", "Hanoi", "north", 21.0285, 105.8522, 30)


def rec(name="Peridot", query="Peridot Grand Hotel, Hanoi, Vietnam"):
    return Record(name=name, category="hotels", area="Hoan Kiem", what="w", why="w",
                  confidence="high", geocode_query=query,
                  sources=["https://a", "https://b"],
                  tier=5, price_low=80.0, price_checked="2026-08-16")


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload
        self.status_code = 200

    def json(self):
        return self._payload

    def raise_for_status(self):
        pass


class FakeSession:
    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.calls = []

    def get(self, url, params=None, headers=None, timeout=None):
        self.calls.append(params["q"])
        return FakeResponse(self.payloads.pop(0))


def hit(lat, lng, cls="tourism"):
    return [{"lat": str(lat), "lon": str(lng), "class": cls, "display_name": "x"}]


def test_accepts_a_hit_near_the_anchor(tmp_path):
    session = FakeSession([hit(21.0333, 105.8480)])
    geo = Geocoder(str(tmp_path / "c.json"), session=session, sleep=lambda s: None)
    result = geo.resolve(rec(), HANOI)
    assert result.accepted is True
    assert result.lat == 21.0333


def test_rejects_a_hit_outside_vietnam(tmp_path):
    paris = hit(48.8566, 2.3522)
    # Every rung resolves to the same out-of-bounds point, so the reason is
    # the same no matter how many fallback rungs the ladder exhausts.
    session = FakeSession([paris, paris, paris, paris])
    geo = Geocoder(str(tmp_path / "c.json"), session=session, sleep=lambda s: None)
    result = geo.resolve(rec(), HANOI)
    assert result.accepted is False
    assert "outside Vietnam" in result.reason


def test_rejects_a_hit_beyond_the_place_radius(tmp_path):
    sapa = hit(22.3364, 103.8440)  # 260 km off
    session = FakeSession([sapa, sapa, sapa, sapa])
    geo = Geocoder(str(tmp_path / "c.json"), session=session, sleep=lambda s: None)
    result = geo.resolve(rec(), HANOI)
    assert result.accepted is False
    assert "30 km" in result.reason


def test_rejects_an_empty_result(tmp_path):
    # Every rung misses; the ladder must exhaust all of them before rejecting.
    session = FakeSession([[], [], [], []])
    geo = Geocoder(str(tmp_path / "c.json"), session=session, sleep=lambda s: None)
    result = geo.resolve(rec(), HANOI)
    assert result.accepted is False
    assert "no match" in result.reason


def test_second_call_is_served_from_cache(tmp_path):
    session = FakeSession([hit(21.0333, 105.8480)])
    geo = Geocoder(str(tmp_path / "c.json"), session=session, sleep=lambda s: None)
    geo.resolve(rec(), HANOI)
    geo.resolve(rec(), HANOI)
    assert len(session.calls) == 1


def test_cache_persists_across_instances(tmp_path):
    cache = str(tmp_path / "c.json")
    first = FakeSession([hit(21.0333, 105.8480)])
    Geocoder(cache, session=first, sleep=lambda s: None).resolve(rec(), HANOI)

    second = FakeSession([])  # would IndexError if it tried to call out
    result = Geocoder(cache, session=second, sleep=lambda s: None).resolve(rec(), HANOI)
    assert result.accepted is True
    assert second.calls == []


def test_it_sleeps_between_live_calls(tmp_path):
    slept = []
    session = FakeSession([hit(21.03, 105.84), hit(21.02, 105.85)])
    geo = Geocoder(str(tmp_path / "c.json"), session=session, sleep=slept.append)
    geo.resolve(rec("A", "A, Hanoi"), HANOI)
    geo.resolve(rec("B", "B, Hanoi"), HANOI)
    assert all(s >= 1.0 for s in slept)
    assert len(slept) == 2


def test_it_sends_an_identifying_user_agent(tmp_path):
    captured = {}

    class Capturing(FakeSession):
        def get(self, url, params=None, headers=None, timeout=None):
            captured.update(headers or {})
            return super().get(url, params=params, headers=headers, timeout=timeout)

    session = Capturing([hit(21.03, 105.84)])
    Geocoder(str(tmp_path / "c.json"), session=session,
             sleep=lambda s: None).resolve(rec(), HANOI)
    assert "vietnam2026" in captured["User-Agent"].lower()


HOIAN_DANANG = Place("hoian-danang", "Hoi An and Da Nang", "central", 15.8801, 108.3380, 40)


def test_fallback_name_city_vietnam_recovers_an_over_specified_miss(tmp_path):
    """Mirrors the diagnosed real failure: an exact query over-specified with
    a district/local-name alias misses, but `name, city, Vietnam` hits."""
    query = "Temple of Literature Van Mieu, Dong Da, Hanoi, Vietnam"
    r = rec(name="Temple of Literature Van Mieu", query=query)
    session = FakeSession([[], hit(21.03, 105.84)])
    geo = Geocoder(str(tmp_path / "c.json"), session=session, sleep=lambda s: None)
    result = geo.resolve(r, HANOI)
    assert result.accepted is True
    assert result.precision == "approximate"
    assert session.calls == [query, "Temple of Literature Van Mieu, Hanoi, Vietnam"]


def test_exact_hit_is_marked_exact_and_uses_one_request(tmp_path):
    session = FakeSession([hit(21.0333, 105.8480)])
    geo = Geocoder(str(tmp_path / "c.json"), session=session, sleep=lambda s: None)
    result = geo.resolve(rec(), HANOI)
    assert result.accepted is True
    assert result.precision == "exact"
    assert len(session.calls) == 1


def test_fallback_hit_beyond_radius_is_still_rejected(tmp_path):
    """Every rung resolves to the same out-of-radius point (Sapa, ~260 km
    from Hanoi) so the ladder must exhaust all rungs and still reject."""
    sapa = hit(22.3364, 103.8440)
    session = FakeSession([sapa, sapa, sapa, sapa])
    geo = Geocoder(str(tmp_path / "c.json"), session=session, sleep=lambda s: None)
    result = geo.resolve(rec(), HANOI)
    assert result.accepted is False
    assert "limit is 30 km" in result.reason


def test_missing_every_rung_makes_all_four_attempts(tmp_path):
    query = "My Tho and Ben Tre candy villages original query, Vietnam"
    r = rec(name="My Tho and Ben Tre coconut candy villages", query=query)
    session = FakeSession([[], [], [], []])
    geo = Geocoder(str(tmp_path / "c.json"), session=session, sleep=lambda s: None)
    result = geo.resolve(r, HANOI)
    assert result.accepted is False
    assert session.calls == [
        query,
        "My Tho and Ben Tre coconut candy villages, Hanoi, Vietnam",
        "My Tho, Hanoi, Vietnam",
        "My Tho, Vietnam",
    ]


def test_cached_rung_does_not_sleep(tmp_path):
    """Rung 1 is a live miss (sleeps once); rung 2 is already cached on disk
    from a prior run and must not sleep or touch the network."""
    cache_path = tmp_path / "c.json"
    cache_path.write_text(
        json.dumps({"Peridot, Hanoi, Vietnam": hit(21.03, 105.84)}),
        encoding="utf-8",
    )
    slept = []
    session = FakeSession([[]])  # only rung 1 should ever reach the network
    geo = Geocoder(str(cache_path), session=session, sleep=slept.append)
    result = geo.resolve(rec(), HANOI)
    assert result.accepted is True
    assert result.precision == "approximate"
    assert slept == [1.0]
    assert session.calls == ["Peridot Grand Hotel, Hanoi, Vietnam"]


def test_compound_place_name_is_truncated_to_its_first_component(tmp_path):
    r = rec(name="Some place", query="Some place, Hoi An and Da Nang, Vietnam")
    session = FakeSession([[], hit(15.88, 108.33)])
    geo = Geocoder(str(tmp_path / "c.json"), session=session, sleep=lambda s: None)
    geo.resolve(r, HOIAN_DANANG)
    assert session.calls[1] == "Some place, Hoi An, Vietnam"


def test_review_queue_lists_every_rejection(tmp_path):
    from kmlpool.geocode import GeocodeResult
    out = tmp_path / "review-queue.md"
    write_review_queue(str(out), [
        ("hanoi", rec("Ghost Hotel"),
         GeocodeResult(None, None, False, "no match for query")),
    ])
    text = out.read_text(encoding="utf-8")
    assert "Ghost Hotel" in text
    assert "no match for query" in text
