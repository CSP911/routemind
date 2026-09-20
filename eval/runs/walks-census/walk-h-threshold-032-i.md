1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m3/body

2. **Answer**
Sign-off: the division director. Quotes: yes — three competing quotes plus a written comparison are required. (Delegation limit for this row is 100,014 thousand KRW; expect about 13 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m3/body

4. **Notes**
The procurement area lists three versions of the approval-threshold table (pre-2024-07-01, 2024-07-01–2025-12-31, and current since 2026-01-01), and the legend-revision page warns explicitly that reaching for the newest is wrong for anything dated before 2026-01-01, and that the oldest version says nothing about being superseded — so it's easy to grab it by mistake if you don't check dates. Today's date (2026-09-20) falls under the current table (`sec-hard-threshold`), so that was the correct one, but this was the one place I deliberately paused to confirm rather than assume. Mapping the three inputs (laptops → C1, ~40M won → V4, 3-year lock-in → M3) was unambiguous once the three legend pages were read — each maps cleanly to one row, and the amount/term legends explicitly matched the wording in the question ("about 40 million won", "locked in for three years") almost verbatim. No ambiguity in the final row itself.
