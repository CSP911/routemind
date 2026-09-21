1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For type E1, tenure T1, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site - likely has monthly accrual and cap/carryover figures"
./bench/rmcli.py overlay add --id ov_2026-09-20_38e5db --address /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l4/body --why "exact row for E1/T1/L4 accrual"
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_38e5db --outcome answered --used /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l4/body

2. **Answer**: You accrue 0.46 days per month. The carry-over limit is 7 days — that is the most you can still be holding (into January, i.e. carried over into the new year).

3. **Source**: /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l4/body

4. **Notes**: The attendance area table listed this row directly by name (`hard-accrual-row-type-e1-tenure-t1-site-l4`), so no legend lookups for what E1/T1/L4 mean were needed — the question already gave the codes. The one place I almost stumbled: the table also lists two superseded accrual versions (`hard-accrual-v2` for 2024-07-01 to 2025-12-31, and an older `leave-accrual`) plus a "legend-revision" warning file about three versions with different figures. Today's date (2026-09-20) falls under the current table (`sec-hard-accrual`, in force since 2026-01-01), so I went straight there and didn't need the revision-history file, but it would be easy to grab a superseded row by mistake if not checking the in-force dates. "How much can I still be holding in January" reads naturally as the carry-over limit — the table doesn't give a separate "January-specific" figure, so I'm treating the 7-day carry-over limit as the answer to that half of the question.
