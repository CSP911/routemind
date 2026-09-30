1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Regular payroll employee, 8 months tenure, Busan branch: monthly leave accrual rate and max carryover/holding into January?" --member /v1/regions/attendance "leave accrual rates, mid-year joiner leave, carryover rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7f4f98 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l2/body

2. **Answer**
You accrue 0.42 days of leave per month. The carry-over limit is 5 days — that is the most you can still be holding when January comes around (any unapproved excess above that is settled at 5 days and the difference is not recoverable).

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l2/body

4. **Notes**
The leave accrual subject has three versions with different date ranges (until 2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend page warns explicitly that reaching for the newest table is wrong for a question dated before 2026-01-01. Today's date (2026-09-20/21) falls inside the current version's range, so `sec-hard-accrual` was correct, but this was a real branch point — a question phrased identically but dated in 2025 would need `hard-accrual-v2` instead, and the oldest version doesn't self-announce that it was superseded, so skipping the revision-legend check would have been an easy way to silently give an answer for the wrong era.

The row table is indexed by three codes (type/tenure/site) with three separate legend pages, and each legend explicitly states it is "the only place the mapping is written down" — no shortcut around fetching all three. "On the regular payroll" mapped cleanly to type E1, "eight months" was listed verbatim as tenure T1, and "Busan branch" as site L2, so no fuzzy nearest-match judgment call was needed here.

One ambiguity worth flagging: "how much can I still be holding in January" was read as asking for the carry-over limit (5 days), i.e., the cap on balance held into the new year — not a request to compute a running total from 8 months of accrual. The row's own text frames the 5-day figure as exactly that cap, which supports this reading, but the question's phrasing could also be misread as asking for a projected balance.
