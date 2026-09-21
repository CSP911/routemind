1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body

2. **Answer**: Which version of the overseas per-diem applies to a 2025-dated claim is written down at `/v1/nodes/hard-perdiem-legend-revision/body`, a page that exists specifically to map date ranges to versions:
- until 2024-07-01 → `overseas-rates` (one qualifier)
- 2024-07-01 to 2025-12-31 → `hard-perdiem-v2` (two qualifiers)
- 2026-01-01 onwards → `sec-hard-perdiem` (current, three qualifiers)

A 2025 claim falls in the middle range, so the applicable version is `hard-perdiem-v2` ("Overseas per-diem, 2024-07-01 to 2025-12-31"), which gives the nightly lodging cap by grade and band (e.g. G1: 95/99/103/107 USD for B1–B4; G2: 111/115/119/123; G3: 127/131/135/139; G4: 143/147/151/155), and notes the daily meal allowance and receipt threshold were unchanged from the older `overseas-rates` rule until 2026-01-01.

3. **Source**:
- /v1/nodes/hard-perdiem-legend-revision/body (which version applies to which dates)
- /v1/nodes/hard-perdiem-v2/body (the applicable version's actual figures)

4. **Notes**: The expense area table itself already warns in its one-line description that there are three per-diem versions with overlapping validity and that the current table is not automatically the right one — that flagged the trap before I even opened a document. It would have been easy to jump straight to `sec-hard-perdiem` (labeled "THE CURRENT OVERSEAS PER-DIEM TABLE") since it's the most prominent per-diem entry in the expense table listing, but it only covers 2026-01-01 onward and would have been the wrong answer for a 2025 date. The legend-revision page exists precisely to prevent that mistake and explicitly calls out both wrong extremes (oldest and current) as traps for a 2025-dated question. No ambiguity beyond that once the legend page was found.
