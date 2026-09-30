1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E4, tenure T1, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/cap rules by employee type, tenure, site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_009ddc --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l2/body

2. **Answer**
Accrues 1.38 days per month. Carry-over limit is 5 days — that is the most that can still be held (carried into January).

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l2/body

4. **Notes**
The leave-accrual subject has three superseded versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly that reaching for the newest is wrong for a question dated before 2026-01-01. Today is 2026-09-20, and the "current" table (`sec-hard-accrual`) has been in force since 2026-01-01, so the January the question asks about (whether meaning the January just passed or the next one) falls inside this version's coverage either way — there was no real ambiguity here once the date was checked, but it's the kind of question where guessing "current" without reading the revision-legend first would have been the wrong instinct if today's date had been earlier.

The row address itself (`hard-accrual-row-type-e4-tenure-t1-site-l2`) matched the three qualifiers (E4, T1, L2) directly, so I didn't need to open the separate site/tenure/type legend files to translate plain-language values into codes — the question was already given in code form.

Minor procedural note: I only added the parent table `/v1/regions/attendance` as an overlay member, not the specific documents I ultimately read, so `overlay close` reported them as "reached" rather than "used" (reached = answered from somewhere the overlay never explicitly named). Doesn't affect the answer, just means the overlay's member list undersold what was actually consulted.
