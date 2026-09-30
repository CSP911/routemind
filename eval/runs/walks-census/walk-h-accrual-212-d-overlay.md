1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E3, tenure T2, site L3, monthly accrual and January max holding of time off" --member /v1/regions/attendance "leave accrual and cap questions live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5378d8 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l3/body

2. **Answer**:
Accrues 1.16 days per month. Carry-over limit (the most that can still be held into January) is 9 days. Notice required to use leave is 6 working days; leave does not accrue during unpaid leave.

3. **Source**:
- /v1/nodes/hard-accrual-legend-revision/body (confirmed today's date, 2026-09-21, falls under the current table, not the superseded versions)
- /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l3/body (the figures: 1.16 days/month accrual, 9-day carry-over limit)

4. **Notes**:
The attendance area's working set surfaced a loud warning file (`hard-accrual-legend-revision`) about three different versions of the leave accrual rules (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) living at different addresses with no indication on the oldest one that it had been superseded. It would have been easy to grab `hard-accrual-v2` by habit or search-order without checking the date. Today's date (2026-09-21) is comfortably inside the current table's range (`sec-hard-accrual`, in force from 2026-01-01), so that risk didn't materialize here, but it's the kind of thing that would silently give a wrong answer for a question dated in 2025.

The question's phrase "how much can I still be holding in January" is not phrased as "carry-over limit" anywhere in the source, so I interpreted it as the carry-over limit (the max balance you can still be holding into the new year) rather than, say, a literal January-specific accrual figure — the table has no month-specific values, only a flat monthly accrual rate and a carry-over cap, so this reading seems like the only one the data supports.

The E3/T2/L3 row address was reachable directly from the `sec-hard-accrual` table listing (64 rows, one per type/tenure/site combination) without needing the separate legend files for type/tenure/site codes, since the question already gave the codes directly rather than descriptive terms.
