from kmlpool.schema import Record, validate_record, validate_hotels, is_shippable


def hotel(**over):
    base = dict(
        name="Peridot Grand", category="hotels", area="Hoan Kiem",
        what="A 5-star boutique hotel on the edge of the Old Quarter, with a "
             "rooftop pool overlooking Hoan Kiem.",
        why="Best rating-to-location ratio of any hotel in the agent proposals",
        confidence="high",
        geocode_query="Peridot Grand Hotel, Hanoi, Vietnam",
        sources=["https://booking.com/a", "https://tripadvisor.com/b"],
        tier=5, tier_official=True, price_low=80.0, price_high=137.0,
        price_checked="2026-08-16",
    )
    base.update(over)
    return Record(**base)


def food(**over):
    base = dict(
        name="Bun Cha Huong Lien", category="food", area="Hai Ba Trung",
        what="A plain three-storey bun cha shop, grilling pork over charcoal "
             "on the street since the 1990s.",
        why="Michelin Bib Gourmand, and the bun cha Hanoi is known for",
        confidence="high",
        geocode_query="Bun Cha Huong Lien, Hanoi, Vietnam",
        sources=["https://guide.michelin.com/x"], kind="vietnamese",
    )
    base.update(over)
    return Record(**base)


def test_valid_hotel_has_no_errors():
    assert validate_record(hotel()) == []


def test_hotel_with_one_source_is_rejected():
    errs = validate_record(hotel(sources=["https://booking.com/a"]))
    assert any("two sources" in e for e in errs)


def test_food_with_one_source_is_accepted():
    assert validate_record(food()) == []


def test_record_with_no_sources_is_rejected():
    errs = validate_record(food(sources=[]))
    assert any("source" in e for e in errs)


def test_missing_why_is_rejected():
    errs = validate_record(food(why=""))
    assert any("why" in e for e in errs)


def test_missing_what_is_rejected():
    errs = validate_record(food(what=""))
    assert any("what" in e for e in errs)


def test_why_that_merely_repeats_what_is_rejected():
    same = "A plain three-storey bun cha shop."
    errs = validate_record(food(what=same, why=same))
    assert any("restate" in e for e in errs)


def test_hotel_over_the_price_cap_is_rejected():
    errs = validate_record(hotel(price_low=250.0, price_high=400.0))
    assert any("200" in e for e in errs)


def test_hotel_at_the_cap_is_accepted():
    assert validate_record(hotel(price_low=200.0, price_high=380.0)) == []


def test_unknown_confidence_is_rejected():
    errs = validate_record(food(confidence="probably"))
    assert any("confidence" in e for e in errs)


def test_three_hotels_in_one_tier_is_rejected():
    hotels = [hotel(name=f"H{i}", tier=5) for i in range(3)]
    errs = validate_hotels("hanoi", hotels)
    assert any("tier 5" in e for e in errs)


def test_two_hotels_per_tier_is_accepted():
    hotels = [hotel(name=f"H{i}", tier=t) for t in (5, 4, 3) for i in range(2)]
    assert validate_hotels("hanoi", hotels) == []


def test_low_confidence_does_not_ship():
    rec = food(confidence="low")
    rec.lat, rec.lng = 21.0, 105.8
    assert is_shippable(rec) is False


def test_record_without_coordinates_does_not_ship():
    assert is_shippable(food()) is False


def test_high_confidence_with_coordinates_ships():
    rec = food()
    rec.lat, rec.lng = 21.0, 105.8
    assert is_shippable(rec) is True
