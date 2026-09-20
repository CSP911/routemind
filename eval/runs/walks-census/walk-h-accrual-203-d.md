1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l4/body

2. **Answer**
You accrue 1.10 days per month. The carry-over limit is 7 days — that is the most you can still be holding when it carries into January.

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l4/body

4. **Notes**
The area index for attendance lists three versions of the leave-accrual subject (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with a warning that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls after the current table's effective date (2026-01-01), so `sec-hard-accrual` is correct here, but this is exactly the kind of question where grabbing the first accrual-looking table without checking the legend-revision page would have risked landing on the superseded `hard-accrual-v2` instead. The phrase "how much can I still be holding in January" reads like it could be asking about a separate carryover-into-new-year policy, but the row itself already states the carry-over limit (7 days) as one of its own fields, so no separate lookup was needed — worth flagging in case the intended answer was actually a different carryover/forfeiture rule elsewhere in the corpus that wasn't surfaced by this path.
