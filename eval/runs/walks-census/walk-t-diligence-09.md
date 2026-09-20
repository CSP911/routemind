1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body

2. **Answer**: For 29 June 2024 (before the 2024-07-01 change, so the original/oldest version of supplier due diligence applies), a new supplier had to pass three checks before registration:
- A sanctions and ownership check against the current restricted-party lists
- A supplier code of conduct acknowledgement, signed by the supplier
- A basic disqualification screen — whether the entity or its owners had been flagged before
A sanctions hit or a refused code of conduct stopped registration outright, with no delegated sign-off able to override it.

3. **Source**: /v1/nodes/supplier-due-diligence/body (version in force until 2024-07-01), identified via /v1/nodes/hard-diligence-legend-revision/body

4. **Notes**: The procurement table's top-level entries for due diligence point at the *current* table (`sec-hard-diligence`, in force from 2026-01-01) and the *second* version (`hard-diligence-v2`, 2024-07-01 to 2025-12-31) — neither is right for 29 June 2024. The legend-revision doc was essential: it states plainly that the oldest version "says nothing at all about having been replaced," so if I'd just opened `supplier-due-diligence/body` cold I could easily have mistaken it for an undated, still-current page rather than a superseded one — or worse, grabbed `hard-diligence-v2` by assuming the earliest listed table in the procurement index was the applicable one. The phrase "two days before the first change" was the key: it meant the 2024-07-01 cutover, so the date falls on the *old* side of that boundary, needing the oldest ("one qualifier") version, not the second.
