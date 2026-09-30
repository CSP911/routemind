1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For type E4, tenure T2, site L1, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type/tenure/site, in force since 2026-01-01" --member /v1/nodes/hard-accrual-legend-revision/body "explains which accrual version applies to which dates" --member /v1/nodes/annual-leave "annual leave entitlement and carryover/cap rules that might explain 'holding in January'"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_8b4f66 --outcome answered --used /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l1/body

2. **Answer**:
For type E4, tenure T2, site L1: accrues 1.44 days per month. The carry-over limit is 7 days — that is the maximum you can still be holding into January (i.e. carried over from the prior year). This is the table in force from 2026-01-01, current as of today (2026-09-21).

3. **Source**:
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l1/body

4. **Notes**:
The attendance area's table flagged up front that leave accrual has THREE versions with different in-force dates (a superseded `hard-accrual-v2` for 2024-07-01 to 2025-12-31, an older `leave-accrual`, and the current `sec-hard-accrual` for 2026-01-01 onward) — easy to grab a stale row if you don't notice that warning. I deliberately picked the current one, and the row itself carries its own "in force from 2026-01-01" footnote confirming it's still current today, so I didn't need to separately open the legend-revision file to be sure.

"How much can I still be holding in January" is ambiguous phrasing — I read it as asking for the carry-over limit (the cap on days held/carried into the new year), since that's the only figure in this row that speaks to a ceiling rather than a monthly flow. There's no separate "January" rule in this row; the carry-over limit is presumably enforced at year-end/start, which January would fall under, but nothing in the document names January specifically.

One mechanical wrinkle: when I created the overlay I named `/v1/nodes/sec-hard-accrual` (the table) as the member, not the specific E4/T2/L1 leaf row — the overlay printout then expanded that table into all of its rows, including the one I actually read. When closing, `rmcli` reported the used address as "reached" rather than "used," because that exact leaf address was never itself passed as a `--member`. No harm to the answer, but worth knowing the overlay tracks membership at the granularity you explicitly name, not at whatever a member table happens to expand into.
