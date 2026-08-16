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
