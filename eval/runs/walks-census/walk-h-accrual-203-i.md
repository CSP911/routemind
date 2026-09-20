1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l4/body

2. Answer
Accrues 1.10 days per month. Carry-over limit into January (or any new period) is 7 days — that is the most you can still be holding.

3. Source
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l4/body

4. Notes
The three phrases in the question ("in three days a week," "been here eight months," "fully from home") are lifted verbatim from the three legend tables' left-hand columns (type, tenure, site respectively) — each mapped to exactly one row (E3, T1, L4) with no need to take a "nearest entry" fallback, so there was no ambiguity there. The one place this could have gone wrong is the date: today is 2026-09-20, and the accrual subject has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) covering different date ranges. I checked the legend-revision page before trusting the current table — 2026-09-20 falls in the "2026-01-01 onwards" band, so `sec-hard-accrual` is correct, but grabbing the newest table without checking that page would have been the wrong reflex for an earlier-dated question. "How much can I still be holding in January" I read as asking for the carry-over limit (7 days), not a projected balance — the row gives no way to compute an actual running total (no start-of-service date, no leave-taken figure), so a projected number would have been invented, not found.
