1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Regular payroll employee, 9 years tenure, Busan branch: monthly leave accrual rate and max carryover/holding into January" --member /v1/regions/attendance "leave accrual and carryover rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_69b1c5 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l2/body

2. **Answer**
Accrues 0.66 days per month. Carry-over limit (the most that can still be held/carried into January) is 14 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l2/body

4. **Notes**
The attendance region lists three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), each superseding the last but none marked as withdrawn — the legend-revision page warns explicitly that reaching for the newest is wrong for any date before 2026-01-01, and that a 2025-dated question needs the middle version, not either extreme. Since today is 2026-09-20/21, the current table (`sec-hard-accrual`, in force from 2026-01-01) is the right one, but this is exactly the kind of thing that's easy to get wrong by habit if you don't check the revision-legend page first. Also worth flagging: the row table has 64 entries indexed by three separate codes (type/tenure/site), each with its own legend doc that must be read before the address can be picked — "regular payroll" → E1, "nine years" → T4 (matches the T4 band exactly), "Busan branch" → L2. None of these required approximation via "nearest entry above," so no ambiguity there. The carry-over limit is what I read as answering "how much can I still be holding in January" — that field is literally named "Carry-over limit, days" in the row, so I'm confident it's the intended figure rather than something else on the page.
