1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l4/body

2. **Answer**: Accrues 0.94 days per month. Carry-over limit is 13 days — that is the most that can still be held over into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l4/body

4. **Notes**: The accrual subject has three superseding versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward), and the legend page warns that reaching for the newest is wrong for dates before 2026-01-01. Today (2026-09-20) falls under the current table, `sec-hard-accrual`, so that part was straightforward — but it would have been easy to grab the current table without checking the version-legend page first, which is exactly the mistake the legend page exists to catch. The three qualifiers (employment type, tenure band, site) are each mapped by a separate legend file rather than being self-evident from the user's phrasing: "two-year contract" only resolves to "type E2" via the legend, not because the row filename says so; "been here five years" maps to tenure T3, not T2 (T2 is literally "two years," a plausible false match if skimming); and "fully from home" maps to site L4. All three had to be resolved before the single matching row (e2-tenure-t3-site-l4) could be addressed — there was no shortcut. The row itself directly answers both halves of the question: the monthly accrual rate and the carry-over limit (interpreted as "how much can still be holding in January," i.e., the cap on days carried into the new year).
