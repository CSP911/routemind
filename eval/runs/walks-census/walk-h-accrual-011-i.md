1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l2/body

2. **Answer**
Accrues 0.50 days per month. Carry-over limit (the most that can still be held into January) is 8 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l2/body

4. **Notes**
Leave accrual has three superseded versions of the same subject at different addresses (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`); the legend-revision page exists specifically to stop you grabbing the wrong one. Today (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is correct — but this is exactly the kind of question where reaching for "the newest" without checking the in-force date would coincidentally be right for the wrong reason.

The real trap was the employment-type legend, not the version: "on the regular payroll" maps to type E1, while "on a two-year contract" maps to type E2. The question's "been here two years" is a tenure detail (which maps cleanly to tenure T2), not an employment-type detail — but the phrase "two years" appearing right next to "regular payroll" is clearly set up to make you misread the questioner as a two-year contractor and pull row E2 instead of E1. Kept them separate: type=E1 (regular payroll), tenure=T2 (two years' service), site=L2 (Busan branch) → row e1-t2-l2.
