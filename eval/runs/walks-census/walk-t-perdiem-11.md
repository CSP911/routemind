## Commands

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/travel-expense
./bench/rmcli.py table /v1/nodes/travel-overseas
./bench/rmcli.py read /v1/nodes/overseas-rates/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py table /v1/nodes/hard-perdiem-v2
```

## Answer

- **2023: USD 180 per night**, for band B (China, South-East Asia, Eastern Europe) — this is the only per-diem version in force in 2023, and it is a plain per-band figure with no grade or stay qualifier.

- **2025: not found as a single figure.** The version in force in 2025 (`hard-perdiem-v2`, 2024-07-01 to 2025-12-31) no longer has a "band B" in the 2023 sense. It indexes lodging by grade and by a *different* band code — B1, B2, B3, B4 — and nothing in RouteMind states that these are subdivisions of the old band B. In fact the only surviving band legend (attached to the 2026 table, not to v2) maps B1 = Tokyo, which was **band A** ("US, Western Europe, Japan") under the 2023 scheme — proof the two letter/number schemes are not nested, just reusing the letter B by coincidence. So there is no defensible single "what band B became" number for 2025; the closest honest answer is the full v2 lodging grid (95–107 USD for grade G1 across B1–B4, rising to 143–155 USD for G4), none of which can be safely singled out as the successor to 2023's band B without an unsupported assumption about which of B1–B4 (if any) corresponds to it.

## Source

- `/v1/nodes/hard-perdiem-legend-revision/body` — which version covers which date
- `/v1/nodes/overseas-rates/body` — 2023 figure (band B, USD 180)
- `/v1/nodes/hard-perdiem-v2/body` — 2025 table (grade × B1–B4 grid)
- `/v1/nodes/hard-perdiem-legend-band/body` — band-code legend (shows B1=Tokyo, revealing the scheme break)

## Notes

The walk has a real trap in it. The legend-revision page correctly steers a 2025 date to `hard-perdiem-v2`, not the current 2026 table — that part is straightforward. The trap is assuming "band B" carries over. `hard-perdiem-v2`'s own columns are literally labeled B1/B2/B3/B4, so it's tempting to just read off the "B1" column as "band B's new value" (95 USD for G1, etc.) — the letter matches and it's the first column. That would have been wrong: the only band legend in the whole knowledge base (`hard-perdiem-legend-band`) is scoped to the *current* 2026 table, not to v2, and it maps B1 to Tokyo — which sat in band A, not band B, under the 2023 scheme. That single fact is enough to show the numbered bands are a completely re-drawn classification, not a refinement of the old A/B/C bands, so picking any of B1–B4 as "band B's successor" is an unsupported guess dressed up as a lookup. I've reported the 2025 side as not resolvable to one figure rather than picking B1 for the coincidence of its letter.
