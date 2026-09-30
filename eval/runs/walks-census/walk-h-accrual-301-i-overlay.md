1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Partner-firm employee, 8 months tenure, Busan branch: monthly leave accrual rate, and max days that can be held/carried into January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site - matches monthly accrual rate question" --member /v1/nodes/hard-accrual-legend-revision/body "explains which accrual version applies to which dates, need to confirm current version applies"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l2/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_db8e2e --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l2/body /v1/nodes/hard-accrual-legend-revision/body

2. **Answer**:
Accrues 1.38 days of leave per month. The carry-over limit (how much can still be held going into January) is 5 days.

3. **Source**:
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t1-site-l2/body
/v1/nodes/hard-accrual-legend-revision/body

4. **Notes**:
The three qualifiers in the question ("here from our partner firm", "been here eight months", "at the Busan branch") mapped exactly and unambiguously to E4/T1/L2 via the three legend pages under /v1/nodes/hard-accrual-legend-*, so no nearest-entry judgment call was needed there.

The one place this could have gone wrong is the revision trap: /v1/nodes/hard-accrual-legend-revision/body warns explicitly that leave accrual has three superseded-but-still-present versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) and that reaching for the newest is only correct if the question's date is on or after 2026-01-01. Today is 2026-09-21, so the current table (`sec-hard-accrual`, in force from 2026-01-01, indexed by three qualifiers) is the right one — but this is exactly the kind of question where grabbing the first accrual-looking row without checking the date would silently give a superseded number. I confirmed via the row's own footer, which restates the same effective-date range, before treating it as final.

"How much can I still be holding in January" reads as the carry-over limit rather than a projected balance — the table gives one static "carry-over limit, days" figure (5) rather than a month-by-month projection, and there's no separate note that this changes specifically for January, so I took the carry-over limit itself as the answer to "how much can I still be holding."
