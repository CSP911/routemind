1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m3/body

2. **Answer**: For category C4, amount V2, term M3 (current table, in force from 2026-01-01): sign-off is by the department head. Yes, other prices are required first — two competing quotes. (Delegation limit: 5054 thousand KRW; working days to expect: 7.)

3. **Source**: /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m3/body — reached via /v1/regions/procurement → /v1/nodes/sec-hard-threshold, with /v1/nodes/hard-threshold-legend-revision/body consulted to confirm which of the three approval-threshold versions applies to today's date (2026-09-20/21).

4. **Notes**: The approval threshold subject has three superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the region table's listing shows both `hard-threshold-v2` (2024-07-01 to 2025-12-31) and the current `sec-hard-threshold` (2026-01-01 onward) side by side with similar-looking names — it would be easy to grab the wrong one without checking the legend-revision page first. The legend-revision page explicitly warns that reaching for the newest is wrong for any question dated before 2026-01-01, which doesn't apply here since today is 2026-09-20/21, but the warning made it clear the date check was mandatory rather than optional. Once on the current table, the row address for C4/V2/M3 was already spelled out exactly in the region listing, so no legend lookups for category/amount/term codes were needed — the address matched the question's terms directly.
