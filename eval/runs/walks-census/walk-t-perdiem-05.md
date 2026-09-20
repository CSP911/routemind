1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-v2/body

2. **Answer**: 115 USD (grade 2, band B2 nightly lodging cap, under the overseas per-diem version in force 2024-07-01 to 2025-12-31).

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body
/v1/nodes/hard-perdiem-v2/body

4. **Notes**: The expense table lists three per-diem-adjacent documents (the legend-revision page, the v2 table, and the current `sec-hard-perdiem` table), and its own row description flags that "the older band-only caps are still here and are superseded" — which nudges toward assuming the current table is the only one that matters. It would have been easy to grab `sec-hard-perdiem` directly since it's labeled "THE CURRENT OVERSEAS PER-DIEM TABLE" and looks authoritative, but that one only applies from 2026-01-01. The legend-revision doc explicitly warns that for a 2025-dated question the answer is the middle version (`hard-perdiem-v2`), not the oldest and not the current one — March 2025 falls inside that document's stated 2024-07-01 to 2025-12-31 window, confirming G2/B2 = 115 USD.
