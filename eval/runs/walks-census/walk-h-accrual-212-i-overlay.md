1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "3 days/week, 2 years tenure, Singapore entity: monthly leave accrual and January carry-forward cap" --member /v1/regions/attendance "leave accrual and carry-forward rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_3a3fc0 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l3/body

2. **Answer**
Accrues 1.16 days of leave per month. Carry-over limit is 9 days — that is the most that can still be held going into January.

3. **Source**
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l3/body

4. **Notes**
This table has three superseded/current versions in force at different date ranges (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), flagged by a legend-revision warning that explicitly says taking either extreme (oldest or newest) without checking the date is the common mistake. Since today is 2026-09-20/21, the current table (`sec-hard-accrual`, in force from 2026-01-01) was the right one — no ambiguity there for this particular question, but it's exactly the kind of thing that would trip up a walk with an older effective date.

The row is selected by three independent legend lookups (employment type, tenure band, site) rather than free text, and the qualifiers ("three days a week", "been here two years", "Singapore entity") map cleanly to E3/T2/L3 with no rounding or nearest-match judgment needed.

The question's second half ("how much can I still be holding in January") reads like it could be asking about a separate carry-forward deadline/rule, but the row itself only exposes one number for this — "Carry-over limit, days: 9" — with no separate January-specific figure, so that is the figure used to answer it.

The overlay close command reported these four addresses as "reached ... from somewhere the overlay never named" — that's because I read them directly rather than first `overlay add`-ing them as members; the answer is correct regardless, but the overlay's working set was left thinner than the actual path taken.
