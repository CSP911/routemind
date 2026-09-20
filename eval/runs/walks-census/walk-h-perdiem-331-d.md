## Commands

    ./bench/rmcli.py table
    ./bench/rmcli.py table /v1/regions/expense
    ./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
    ./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s2/body

## Answer

Hotel (lodging) cap: 339 USD per night.
Receipt required above: 60 USD (receipt threshold).

## Source

- /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s2/body

## Notes

The path was direct — the top-level `expense` area's own listing flags a per-diem
"revision" warning (three versions with different date ranges) and even lists a
superseded version (`hard-perdiem-v2`) right alongside the current one, so it would
have been easy to open the wrong version. The current table (`sec-hard-perdiem`)
states plainly it's the one in force from 2026-01-01, which matches today's date
(2026-09-20), and the row itself repeats that in-force date, so there was no real
ambiguity once inside the right table — but a careless reader skimming the expense
area listing could easily grab `hard-perdiem-v2` by mistake since its description
also looks plausible at a glance. The G4/B4/S2 row existed exactly as named, no
lookup through the grade/band/stay legends was needed.
