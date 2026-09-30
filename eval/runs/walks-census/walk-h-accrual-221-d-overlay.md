1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E3, tenure T3, site L2, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/cap rules by employee type, tenure, and site"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_871795 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l2/body

2. **Answer**:
For type E3, tenure T3, site L2 (current table, in force from 2026-01-01): accrues 1.22 days per month. Carry-over limit is 11 days — that is the cap on what can still be held into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l2/body

4. **Notes**:
Leave accrual has three versions in effect for different date ranges (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend-revision page warns explicitly that reaching for the newest is wrong unless the question's date actually falls in the current window. Today's date (2026-09-20/21) falls in the current window, so the `sec-hard-accrual` table was the right one — but this was the one place a wrong reflex (always grab the newest) would have coincidentally still been right, which is exactly why the legend page needed checking rather than assumed. The row address matched the E3/T3/L2 qualifiers in the question exactly, so no legend lookup for code meanings was needed. The overlay close output flagged both used addresses as "reached … from somewhere the overlay never named" since I fetched them via table/read navigation rather than formally `add`-ing them to the overlay first — worth noting as a quirk of the tool, not an error in the answer.
