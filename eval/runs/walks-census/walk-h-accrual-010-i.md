## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l1/body

## Answer
Accrues 0.48 days per month. Carry-over limit is 7 days (the most you can still be holding into January).

## Source
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l1/body

## Notes
Leave accrual has three versions in force over different date ranges, flagged by hard-accrual-legend-revision — the oldest version doesn't say it was superseded, so checking the date against that legend before picking a table mattered. Today (2026-09-20) falls under the current table (sec-hard-accrual, in force since 2026-01-01), so no ambiguity there.

The real trap was the tenure legend: "been here two years" maps to tenure T2, and it would be easy to confuse that with employment "type E2" ("on a two-year contract") since both use the digit 2. "On the regular payroll" is a separate axis (employment type) and maps to E1, not E2 — the two "two"s in the question (regular payroll vs. two years) refer to different qualifiers and must not be collapsed into one. Row is type E1 / tenure T2 / site L1.
