1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Regular payroll, 5 years tenure, Seoul office: monthly leave accrual rate and how much can be held/carried into January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site - likely has the monthly accrual rate" --member /v1/nodes/hard-accrual-legend-revision/body "warns of 3 versions of accrual table with different dates - need to confirm which applies" --member /v1/nodes/annual-leave "entitlement and booking - may cover carryover/holding cap into January"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a117bc --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l1/body

2. **Answer**: Accrues 0.56 days per month. Carry-over limit (the most that can be held over into January) is 10 days.

3. **Source**:
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l1/body

4. **Notes**: The three qualifiers (employment type, tenure band, site) are each looked up in a separate legend file, and none of the legend text repeats the plain-language description used in the row filenames — you have to translate "on the regular payroll" → E1, "been here five years" → T3, "at the Seoul office" → L1 before the row address (hard-accrual-row-type-e1-tenure-t3-site-l1) even makes sense. It would be easy to skip the legends and guess the row from intuition (e.g. assuming "regular payroll" means something other than E1), which the legend files explicitly warn against ("the leave accrual rows are indexed by the value in the right-hand column and do not repeat what is in the left"). Also had to check hard-accrual-legend-revision because there are three versions of this table (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) — since the question is dated 2026-09-20, the current table (sec-hard-accrual) is correct, but a question dated in 2025 would need the superseded hard-accrual-v2 instead. The row itself directly answered both parts of the question (monthly accrual and carry-over limit), so the broader annual-leave/leave-use tables added to the overlay turned out to be unnecessary.
