1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l2/body

2. Answer

Accrues 0.90 days per month. Carry-over limit (the most that can be held/carried into January) is 11 days.

3. Source

/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l2/body

4. Notes

The leave accrual subject has three superseded versions indexed by different numbers of qualifiers (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01, and that a 2025 date needs the middle version — not the oldest, not the current. Today's date (2026-09-20) is after the 2026-01-01 cutoff, so the current table (`sec-hard-accrual`) is correct here, but this was the one place a careless walk could go wrong (grabbing the current table by reflex without checking the effective date first).

The three qualifiers had to be resolved through three separate legend files before the row address could be built (type: "two-year contract" → E2; tenure: "five years" → T3; site: "Busan branch" → L2). Each legend states plainly it is "the only place the mapping is written down," so guessing the codes instead of reading them would have been a mistake even though the mapping looks obvious in hindsight.

The row page frames "carry-over limit" as the figure that answers "how much can I still be holding," which matches the question's phrasing well enough that no further table was needed.
