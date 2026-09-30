1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "3 days/week part-time, 9 years tenure, Busan branch: monthly accrual rate and January carryover cap for time off?" --member /v1/regions/attendance "part-time accrual and carryover rules for leave are covered under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_d362b3 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l2/body

2. **Answer**
Accrues 1.30 days of leave per month. Carry-over limit is 14 days — that is the most you can still be holding into January (any unapproved excess beyond 14 is settled at that figure and not recoverable; an unavoidable excess needs a short written statement and is decided by the budget holder).

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l2/body

4. **Notes**
The accrual table exists in three versions with different rules, and only a legend page (hard-accrual-legend-revision) says so — the current table's own listing doesn't warn you it superseded anything until you're already reading it. Today's date (2026-09-20) falls after the 2026-01-01 cutover, so the current table (sec-hard-accrual) is the right one; a question dated in 2025 would need hard-accrual-v2 instead, which is an easy version to grab by mistake since only the dates in the legend distinguish them.

The three qualifiers (type, tenure, site) are each mapped by a separate legend page, and none of the row addresses are guessable from plain English — "three days a week" only resolves to E3 by reading hard-accrual-legend-type, "nine years" only resolves to T4 (the top band, not an approximation) by reading hard-accrual-legend-tenure, and "Busan branch" only resolves to L2 by reading hard-accrual-legend-site. Nine years happened to land exactly on the T4 label rather than needing the "nearest lower band" fallback the legends describe, so no judgment call was needed there — but it would be easy to assume the nearest-band fallback applies when it doesn't.
