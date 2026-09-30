1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "regular payroll, 2 years tenure, fully remote/WFH: monthly leave accrual rate, and max carryover/balance holdable in January" --member /v1/regions/attendance "leave accrual, carryover cap questions live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_096c2e --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l4/body

2. **Answer**:
Accrues 0.54 days of leave per month. The carry-over limit (max that can still be held going into January) is 10 days. Notice required to take leave is 2 working days; this type of leave does not accrue during unpaid leave.
(Row: type E1 / tenure T2 / site L4, in force from 2026-01-01, current version.)

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l4/body

4. **Notes**:
The leave accrual subject has three superseded/current versions indexed separately (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and the legend-revision page warns explicitly against reflexively grabbing the newest table — for a question dated in 2025 the middle version would be correct instead. Since this question is being asked today (2026-09-20/21), the current table (`sec-hard-accrual`, in force from 2026-01-01) was the right pick, but this was the one place in the walk worth double-checking rather than assuming. The row is indexed by three separate qualifiers (type/tenure/site) each with its own legend translating plain-language descriptions ("on the regular payroll" → E1, "been here two years" → T2, "fully from home" → L4) — skipping any one legend and guessing the code would have risked pulling the wrong row silently, since there's no cross-check built into the row itself. The "how much can I still be holding in January" phrasing maps to the row's "carry-over limit" field, not a separate January-specific figure — there's no distinct January entry, so I read it as the standing carryover cap.
