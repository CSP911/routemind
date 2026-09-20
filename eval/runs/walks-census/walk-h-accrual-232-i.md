1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l3/body

2. **Answer**
Accrues 1.32 days per month. Carry-over limit (the most that can still be held into the new year, e.g. January) is 15 days.

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirms the current, 2026-01-01-onwards table is the right version for today's date)
- /v1/nodes/hard-accrual-legend-type/body (three days a week → type E3)
- /v1/nodes/hard-accrual-legend-tenure/body (nine years → tenure T4)
- /v1/nodes/hard-accrual-legend-site/body (Singapore entity → site L3)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l3/body (the figures: 1.32 days/month accrual, 15 days carry-over limit)

4. **Notes**
The subject has three superseded/current versions of the accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns the oldest version doesn't admit it's been replaced — it would be easy to land on it by accident via a stale link or search hit. Checking today's date (2026-09-20) against the revision table before reading any figures was necessary to confirm `sec-hard-accrual` (in force from 2026-01-01) is correct, not `hard-accrual-v2`. Also, the row's own legend is indexed by three separate qualifier tables (type, tenure, site) that must each be resolved before the row address can be built — "three days a week" isn't a tenure or site value, it's the *type* qualifier, which wasn't obvious from the question's phrasing alone since "three days a week" more naturally suggests a work-schedule/attendance fact rather than an employment-type classification. Getting that mapping wrong (e.g. mistaking it for something schedule-related) would have pointed at the wrong row entirely.
