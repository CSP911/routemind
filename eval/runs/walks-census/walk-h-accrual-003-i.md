1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l4/body

2. **Answer**
Accrues 0.46 days of leave per month. Carry-over limit is 7 days — that is the maximum that can still be held (carried into January).

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l4/body

4. **Notes**
The attendance table's legend-revision file warns that leave accrual has three superseded versions and that reaching for the newest one is wrong for any date before 2026-01-01 — easy to grab the wrong table if you skip that check. Since today (2026-09-20) falls after 2026-01-01, the current table (`sec-hard-accrual`) is correct here, but this is exactly the trap the walk warns about. All three qualifiers ("regular payroll" → E1, "eight months" → T1, "fully from home" → L4) matched the legend wording exactly, so no ambiguous nearest-entry judgment call was needed. The phrase "how much can I still be holding in January" reads like it might be asking about a specific year-end/January proration rule, but the row only exposes one relevant figure — the carry-over limit (7 days) — which is the cap on what survives into the new year; there was no separate "January" figure to find.
