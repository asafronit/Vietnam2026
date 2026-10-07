# Vietnam 2026 — KML map pool

Generates five Google My Maps KML files from researched YAML.

## Run

    PYTHONPATH=src .venv/Scripts/python.exe -m kmlpool.cli geocode
    PYTHONPATH=src .venv/Scripts/python.exe -m kmlpool.cli build
    PYTHONPATH=src .venv/Scripts/python.exe -m kmlpool.cli verify

## Edit content

Edit `data/<place>.yaml`. Never edit `out/*.kml` — it is regenerated.
After editing, rerun all three commands. Geocoding is cached, so only
new or changed `geocode_query` values cost a network call.

## Import

mymaps.google.com, create one map, Import, upload
`out/vietnam-2026-pool.kml`. Seven layers appear, all toggleable.

My Maps has no hierarchy beyond map, layer, feature — there are no
sub-layers, so the seven layers are deliberately flat.

## Rules the build enforces

- Hotels need two independent sources; everything else needs one.
- Hotel `price_low` must be 200 USD or less.
- At most two hotels per star tier per place.
- `confidence: low` records stay in YAML and never reach the KML.

## Transfers

Inter-city transfers live in `data/transfers/<from>__<to>.yaml`, one file per
pair, and are exported by the same `web` command to `out/transfers-data.js`
(`const TRANSFERS_DATA = [...]`). A transfer is not a place: it never enters
`poi-data.js`, its counts, the map or search. Model and rules:
`src/kmlpool/transfers.py`.

Each file holds `from`, `to` (station ids from `places.yaml`), `reverse_ok`,
an optional `note`/`note_he`, and a list of `options` -- one per way to make
the trip (`mode`: flight, train, sleeper_train, sleeper_bus, limousine_van,
bus, private_car, boat, speedboat, combo).

Rules the build enforces (a broken transfer fails `web` *and* `build`, and
nothing is written):

- `from`/`to` are real station ids and differ; one file per pair.
- Every option has a `board` with a name and a Latin-script address. Unless
  `pickup_hotel: true`, it also needs `lat`/`lng` inside Vietnam -- they feed
  the Grab button on the site.
- `duration_min` (minutes) and `price_low` are required; `*_max`/`*_high`
  may not be lower. `currency` is VND or USD, quoted as found -- the site
  converts. `price_unit` is per_person, per_vehicle or per_cabin.
- At least one source and a `checked` ISO date per option.
- Hebrew is mandatory: `pros_he`/`cons_he` item for item, `tips_he` and
  `note_he` whenever the English exists.
- `book_links` is a list of `{name, url}`, one per company that sells the
  trip (a flight route gets one per airline); every url is https.
- Vietjet is never offered: an operator or booking link naming it fails.
- Flights go in as `mode: flight` wherever both ends have an airport, boarded
  at the departure airport (with coordinates, so Grab can get you there).
  Where there is no flight, say so in `note`.
- `confidence: low` options never ship; a transfer left with none is dropped.
