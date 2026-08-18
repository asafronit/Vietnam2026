# Spike Findings — My Maps KML fidelity

Date: ______________  Account: ______________

**Probe file:** `kml/spike/probe.kml` (validated well-formed: 3 folders, 3 styles,
2 points, 1 line)

## How to run it

1. Open <https://mymaps.google.com> and create a new map.
2. Click **Import**, upload `kml/spike/probe.kml`.
3. Answer the five questions below.

## Questions

Answer each Yes/No plus one sentence.

**1. Did the three `<Folder>` elements become three separate layers?**
`LAYER A - Hotels`, `LAYER B - Food`, `LAYER C - Route`

    YES / NO
    If NO — how many layers appeared, and what were they named?
    >

**2. Did `IconStyle` `<color>` tint the pins?**
Hotel pin should be gold/amber, food pin should be green.

    YES / NO
    >

**3. Did the custom `<Icon><href>` icons render?**
Hotel pin should be a bed, food pin should be cutlery.

    YES / NO
    >

**4. Did HTML in `<description>` render, and is the `<a>` link clickable?**
Click the hotel pin. Bold "5-star", italic "(indicative…)", working Booking link.

    YES / NO
    >

**5. Did the `LineString` render with its colour and width?**
A thick purple line from Hanoi to Sapa.

    YES / NO
    >

## Decision

- **Q1 YES** → one file, seven layers, one import. Task 5 default path.
- **Q1 NO** → seven files, one per layer, all imported into the same map.
  Task 5 branch B. End result on the phone is identical.

Q2–Q5 shape the styling only; whatever does not survive gets dropped from
`style.py` rather than emitted uselessly.

    Decision:
    >

---

## ANSWERED — 2026-08-18, from Asaf's live import

1. **Did the three `<Folder>` elements become separate layers?** **YES.**
   Confirmed on the real 7-layer pool file: all seven appeared as separate,
   independently toggleable layers. Task 5 Branch A was correct; Branch B is
   dead and needs no implementation.

2-3. Icon colour and custom icon rendering — not separately reported.

4. **Did HTML in `<description>` render with clickable links?** Partially.
   `https://` links work. **A custom URI scheme does NOT** — `grab://` renders
   as dead, unclickable text. My Maps sanitises non-http(s) schemes.

5. LineString — not separately reported; the route line is present.

## Consequence
Any "take me there" action inside a KML description must use `https://`.
Replaced the Grab deep link with a Google Maps directions URL.
