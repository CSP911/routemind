1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l3/body

2. **Answer**:
For type E1, tenure T4, site L3 (current table, in force from 2026-01-01): you accrue 0.68 days per month, and the carry-over limit is 15 days — that is the most you can still be holding when carrying into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to today's date, 2026-09-20)
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l3/body (the figures)

4. **Notes**:
The attendance area lists three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no indication on the current table itself that older versions exist until you've already found it — the legend-revision page is what stops you from just grabbing the first "leave accrual" hit. Today's date (2026-09-20) is safely inside the current version's range (2026-01-01 onward), so this case wasn't ambiguous, but it would have been easy to skip that check since the question gave codes (E1/T4/L3) that look like they point straight at one row. The question's second half ("how much can I still be holding in January") isn't phrased as "carry-over limit," so it's easy to misread as asking for a separate January-specific accrual rule; the row's "Carry-over limit, days" field is the only field that matches that meaning, and there was no separate January-specific document to cross-check it against.
