1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In three days a week, been here eight months, at the Seoul office: how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual and carryover rules likely live here"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_79e7fe --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l1/body

2. **Answer**
You accrue 1.04 days per month, and can carry over (hold) up to 4 days into January.

3. **Source**
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t1-site-l1/body

4. **Notes**
The three plain-language qualifiers in the question ("three days a week", "eight months", "Seoul office") each had to be translated through a separate legend file before the actual accrual row could be addressed — "three days a week" maps to type E3 (not, as I first assumed, a part-time/prorated category; the legend just calls it that), "eight months" maps to tenure T1, and "Seoul office" maps to site L1. Getting any one of these wrong silently points at a different row with different numbers, and nothing in the row itself warns you if you picked the wrong qualifier.

The bigger risk was picking a stale accrual table: the attendance area's working set surfaced three separate accrual documents — `sec-hard-accrual` (current, in force 2026-01-01 onward), `hard-accrual-v2` (superseded, 2024-07-01 to 2025-12-31), and a `hard-accrual-legend-revision` note warning of three versions total. Today's date (2026-09-20/21) falls under the current table, so `sec-hard-accrual` was correct, but it would have been easy to grab `hard-accrual-v2` by mistake since both showed up together in the same listing.

The overlay close output labeled the four addresses I used as "reached ... from somewhere the overlay never named" — this is just the tool's generic definition of that tag, not a real discrepancy; those exact addresses were already visible in the initial overlay table under the attendance member, so nothing was actually reached from outside the named working set.
