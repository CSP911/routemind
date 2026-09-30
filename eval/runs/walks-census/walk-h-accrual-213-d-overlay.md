1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E3, tenure T2, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/cap questions live under attendance"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5d2561 --outcome answered --used /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l4/body

2. **Answer**
You build up 1.18 days of leave per month under type E3, tenure T2, site L4. The carry-over limit is 10 days, so that is the most you can still be holding once the new year (January) rolls in.

3. **Source**
/v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l4/body

4. **Notes**
The E3/T2/L4 combination named in the question maps directly to one row's address in the accrual table (`hard-accrual-row-type-e3-tenure-t2-site-l4`), so no legend lookup was needed to translate qualifiers into codes — the question already gave codes, not descriptions.

The bigger risk here was versioning: the attendance overlay surfaced three accrual tables (`leave-accrual`, `hard-accrual-v2` for 2024-07-01–2025-12-31, and `sec-hard-accrual` for 2026-01-01 onward) with an explicit warning node about picking the wrong one. Today's date (2026-09-20) falls inside the current table's effective range, so `sec-hard-accrual` was correct, but it would be easy to grab a superseded row if you didn't notice the warning node or check the in-force dates.

"How much can I still be holding in January" reads like it could mean two different things — a forward-looking cap on carryover into next January, or something tied to a specific "days that decide money" concept (there's a sibling row for that in the attendance area). I treated it as the plain carry-over limit field, which the row states explicitly (10 days) and which is the natural reading of "holding" leave balance — no separate January-specific rule appeared anywhere in this row or its siblings.
