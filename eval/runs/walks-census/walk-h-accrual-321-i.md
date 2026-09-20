1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l2/body

2. **Answer**
Accrues 1.54 days per month. Carry-over limit (the most that can still be held going into January) is 11 days.

3. **Source**
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l2/body

4. **Notes**
"Here from our partner firm" maps directly to type E4 via the legend's exact wording — no ambiguity there. "Been here five years" and "at the Busan branch" also matched their legend rows exactly (T3, L2), so no nearest-entry guessing was needed. The one place this could have gone wrong is the version check: the accrual subject has three superseded/current versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls inside the current table's window (2026-01-01 onward), so `sec-hard-accrual` was correct here, but this is clearly a trap for questions dated in 2025 — I checked the revision page deliberately rather than assuming the current table applied. The question's second half ("how much can I still be holding in January") is answered by the row's carry-over limit field, not a separate document — nothing else in the attendance area addresses carry-over caps by these same three qualifiers, so I'm treating this single row as sufficient for both parts of the question.
