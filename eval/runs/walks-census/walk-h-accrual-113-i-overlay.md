1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two-year contract, two years tenure, fully remote: monthly leave accrual and max carryover into January?" --member /v1/regions/attendance "leave accrual and carryover rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_340083 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l4/body

2. **Answer**
You accrue 0.86 days per month. The carry-over limit is 10 days — that is the most you can still be holding when January comes around (any unapproved excess above that is settled at the limit and the difference is not recoverable).

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l4/body

4. **Notes**
The legend-revision page is the thing to check first and not skip: leave accrual has three versions with different dates, and only the current one (`sec-hard-accrual`, in force from 2026-01-01) applies to a question dated today. Reaching for the newest table without checking would have been right this time, but only by luck — the warning is explicit that for a 2025-dated question the middle version (`hard-accrual-v2`) is the correct one, not the current or oldest.

The row lookup also required decoding all three qualifiers separately from their own legend files before picking one of 64 rows — "two-year contract" maps to type E2 (not to be confused with "here two years," which is a tenure fact, not an employment-type fact), "been here two years" maps to tenure T2, and "fully from home" maps to site L4. It would be easy to conflate the two "two year" phrases (contract length vs. tenure) since they use the same number; they land in different legend tables (type vs. tenure) and both had to be resolved independently.

The overlay close call reported all five read addresses as "reached ... from somewhere the overlay never named" rather than as matched members — I never ran `overlay add` for them after drilling down from the table, only the original attendance-region membership was recorded. This didn't block answering, but it means the overlay's working set undersells the actual path taken; if precision matters, add each drill-down address as a member before closing.
