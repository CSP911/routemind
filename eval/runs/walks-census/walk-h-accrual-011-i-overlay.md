1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Regular payroll employee, 2 years tenure, Busan branch: monthly leave accrual rate and max carryover/holding into January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type/tenure/site, in force 2026-01-01" --member /v1/nodes/hard-accrual-legend-revision "warns which accrual version covers which dates, need to confirm today's date falls under current table"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_bd3edb --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l2/body

2. **Answer**
For a regular-payroll employee (type E1), two years' tenure (T2), at the Busan branch (site L2):
- Accrues 0.50 days per month.
- Carry-over limit is 8 days — that is the most that can be held over into January.
This is under the current accrual table, in force from 2026-01-01, which applies to today's date (2026-09-21).

3. **Source**
- /v1/nodes/hard-accrual-legend-type/body (maps "regular payroll" → type E1)
- /v1/nodes/hard-accrual-legend-tenure/body (maps "two years" → tenure T2)
- /v1/nodes/hard-accrual-legend-site/body (maps "Busan branch" → site L2)
- /v1/nodes/hard-accrual-legend-revision/body (confirms current table applies to today's date)
- /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l2/body (the accrual and carry-over figures)

4. **Notes**
The attendance area's table lists the accrual subject three times (superseded, v2, and current), each
with a loud warning to check the date before trusting the newest one — easy to grab the wrong version
if the question were dated in 2025 instead of now. The accrual rows are indexed by three qualifiers
(employment type, tenure band, site) that are never spelled out in plain English anywhere except three
separate legend files — "regular payroll," "two years," and "Busan branch" only resolve to E1/T2/L2 by
reading all three legends first. It would be easy to guess a mapping (e.g. assume "regular payroll"
means something about pay frequency rather than employment classification) instead of checking the
legend, which is the one place that mapping is actually written. The overlay's own members list only
had the two top-level table/legend addresses I initially guessed as relevant; the actual leaves used
(the three legend files and the specific row) were never added as overlay members, so the close command
reported them as "reached" rather than as named working-set entries — worth adding them as members
during the walk next time rather than at the end.
