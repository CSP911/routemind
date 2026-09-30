1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Singapore partner firm employee, 5 years tenure: monthly leave accrual rate and max carry-forward into January" --member /v1/regions/attendance "leave accrual rate and carryover cap are attendance topics"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e784e4 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l3/body

2. **Answer**
Accrues 1.56 days of leave per month. The carry-over limit is 12 days — that is the maximum that can still be held going into January. (Notice required to take leave: 7 working days; leave does not accrue during unpaid leave.)

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t3-site-l3/body

4. **Notes**
Leave accrual has three superseded versions (`leave-accrual`, `hard-accrual-v2` for 2024-07-01–2025-12-31, and `sec-hard-accrual` current from 2026-01-01). Today's date is 2026-09-21, which falls inside the current version's range, and the "January" being asked about (the next one, January 2027) is also still covered by it, so no version-switching was needed here — but it would have been the wrong move to skip checking the revision legend and just assume "current" was right by reflex.

The three qualifiers all needed legend lookups rather than being obvious from the question's wording: "here from our partner firm" maps to type E4 (not, say, E2's "two-year contract," which is a different arrangement entirely), "been here five years" maps to tenure T3, and "in the Singapore entity" maps to site L3. Getting any one of these wrong (e.g. assuming partner-firm staff fall under the regular-payroll row E1) would silently point at a different row with different numbers, since the table has 64 near-identical rows differing only by these codes.
