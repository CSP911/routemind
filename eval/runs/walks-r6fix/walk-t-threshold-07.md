1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/approval
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**: The approval threshold has been written three times (two rewrites after the original):
   - Until 2024-07-01 — original version (`threshold-table`, in approval; indexed by one qualifier)
   - 2024-07-01 to 2025-12-31 — second version (`hard-threshold-v2`, moved to procurement; indexed by two qualifiers)
   - From 2026-01-01 onwards — current version (`sec-hard-threshold`, in procurement; indexed by three qualifiers)

3. **Source**:
   - /v1/nodes/hard-moved-threshold/body
   - /v1/nodes/hard-threshold-legend-revision/body

4. **Notes**: The approval region's table listing already flags that "spend thresholds by amount moved to procurement on 2026-01-01 — what is still here is the old rule," which is the first sign this isn't a single-answer lookup. Opening `hard-moved-threshold/body` in approval gives the three-version breakdown but explicitly defers to `hard-threshold-legend-revision` in procurement as "the full version table," so I followed that pointer rather than stopping at the first hit — the approval-region copy would have been enough to answer the count/dates, but it isn't the authoritative table and says so itself. Easy trap here: the region table in procurement lists both `hard-threshold-legend-revision` and `hard-threshold-v2` as separate files — grabbing `hard-threshold-v2` alone would only give the middle version, not the full history. The legend/revision file was the one with the complete three-row table.
