1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body

2. **Answer**: For a claim dated in 2025, the applicable version is the second (middle) one, "Supplier due diligence, second version," in force 2024-07-01 to 2025-12-31, at address `hard-diligence-v2`. It is indexed by two qualifiers — origin and value — with checks-required figures:

| origin \ value | W1 | W2 | W3 | W4 |
|---|---|---|---|---|
| O1 | 30 | 31 | 32 | 33 |
| O2 | 34 | 35 | 36 | 37 |
| O3 | 38 | 39 | 40 | 41 |
| O4 | 42 | 43 | 44 | 45 |

All other elements (checks beyond this table, documents to collect, re-review interval) carried over unchanged from the oldest version until 2026-01-01. The current table (`sec-hard-diligence`, from 2026-01-01, three qualifiers including goods) and the oldest table (`supplier-due-diligence`, until 2024-07-01, one qualifier) do NOT apply to a 2025 date.

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (the version map — identifies which of the three versions covers 2025)
- /v1/nodes/hard-diligence-v2/body (the actual middle-version content and figures)

4. **Notes**: The procurement table lists three separate due-diligence documents (oldest `supplier-due-diligence`, middle `hard-diligence-v2`, current `sec-hard-diligence`) plus a `hard-diligence-legend-revision` page that exists solely to map dates to versions. The trap here is exactly what the legend warns about: it would be easy to grab the current table (`sec-hard-diligence`, prominently labeled "THE CURRENT SUPPLIER DUE DILIGENCE TABLE") since it's the most emphasized entry in the procurement listing, but that only applies from 2026-01-01 onward. The legend explicitly states the oldest version "says nothing at all about having been replaced," so reading the oldest doc alone (without checking the legend first) would give false confidence that it's still current. Checking the legend before picking a version was the right move and avoided both wrong extremes.
