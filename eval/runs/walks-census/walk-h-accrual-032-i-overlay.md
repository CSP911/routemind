1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Singapore entity, regular payroll, 9 years tenure: monthly leave accrual rate and max carryover/holding cap in January" --member /v1/regions/attendance "leave accrual, carryover, and holding cap questions live under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_bd9fc9 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l3/body

2. **Answer**
0.68 days accrue per month. The carry-over limit (the most that can still be held into January) is 15 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l3/body

4. **Notes**
The near-miss here was the version trap: this domain has three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) covering different date ranges, and the legend page warns explicitly that reaching for the newest one is wrong for anything dated before 2026-01-01. Today's date (2026-09-20/21) falls inside the current version's range (2026-01-01 onward), so `sec-hard-accrual` was correct, but this is exactly the kind of question where grabbing the first accrual-looking table without checking the revision legend would have silently produced the wrong year's numbers.

The other place to be careful was translating the plain-language question into the row's three qualifiers: "regular payroll" only maps to type E1 via the type legend (it's not a self-evident label), "nine years" maps cleanly to tenure T4 since it's listed verbatim, and "Singapore entity" maps to site L3. None of these codes could be guessed without reading the legend files first — the row addresses are literally built from them, so skipping the legends would have meant either failing to construct a valid address or guessing wrong.

One phrase in the question, "how much can I still be holding," reads at first like a request for a current leave balance rather than a policy limit — but that number isn't something this table (or this domain generally, per the region table's description) tracks per person; the attendance table's carry-over limit is the fixed policy cap, which is what the question is actually asking for since no personal balance was given or requested elsewhere.
