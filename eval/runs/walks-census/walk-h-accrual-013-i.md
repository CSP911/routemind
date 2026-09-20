1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l4/body
```

2. **Answer**
Accrues 0.54 days per month. Carry-over limit is 10 days — that is the most you can still be holding into January.
(Row: type E1 "on the regular payroll", tenure T2 "been here two years", site L4 "fully from home".)

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-accrual-legend-type/body
- /v1/nodes/hard-accrual-legend-tenure/body
- /v1/nodes/hard-accrual-legend-site/body
- /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l4/body

4. **Notes**
The legend-revision page is the load-bearing step here — there are three superseded/current versions of the accrual rules (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) and the oldest one never says it was replaced, so grabbing the first hit for "leave accrual" without checking dates would silently give a stale answer. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is correct.

The type legend is a trap: "on a two-year contract" is its own row (type E2), separate from tenure length. The question's "regular payroll" phrasing maps cleanly to E1, not E2 — but it would be easy to misread "two years" in the question and jump to E2 by pattern-matching on the number rather than reading what "regular payroll" actually selects. Tenure T2 ("been here two years") is the correct place the "two years" detail belongs, and it happened to match a legend entry exactly, so no nearest-neighbor judgment call was needed there. Site legend also matched "fully from home" exactly to L4, no ambiguity.

The row page also carries an "if figures are exceeded" clause about unapproved excess, but the question only asked for the monthly accrual and the carry-over cap, so that wasn't included in the answer.
