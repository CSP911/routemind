1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For type E3, tenure T4, site L3, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site since 2026-01-01" --member /v1/nodes/hard-accrual-legend-revision/body "clarifies which accrual version applies to which dates"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l3/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_baf32d --outcome answered --used /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l3/body /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**:
For type E3, tenure T4, site L3: accrues 1.32 days per month, with a carry-over limit of 15 days — that is the most that can be held at any point, including into January.

3. **Source**:
/v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l3/body
/v1/nodes/hard-accrual-legend-revision/body

4. **Notes**:
There are three versions of the accrual table (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each in force for a different date range, and the oldest one gives no indication it was ever superseded. It would be easy to grab the wrong version if the question's date weren't checked against the legend page first. Today (2026-09-21) falls under the current table, `sec-hard-accrual` (in force from 2026-01-01), which is the one indexed by all three qualifiers (type, tenure, site) — matching this question's E3/T4/L3. The row itself doesn't use the word "January" — the "carry-over limit" figure is what answers "how much can I still be holding," and I inferred that this cap applies year-round (including at the January boundary) rather than being a January-specific rule; there was no separate January-specific carry-over note anywhere in this row or the legend to contradict that reading.
