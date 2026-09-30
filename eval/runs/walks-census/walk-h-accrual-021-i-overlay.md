1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Regular payroll employee, 5 years tenure, Busan branch: monthly leave accrual rate and max carryover holding in January?" --member /v1/regions/attendance "leave accrual and carryover rules likely live in attendance area"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5491a4 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l2/body

2. **Answer**:
Accrues 0.58 days per month, and can hold a maximum of 11 days carried over (as of the current table, in force from 2026-01-01).

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l2/body

4. **Notes**:
The accrual subject has three superseding versions (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and it would have been easy to grab the newest table on reflex without checking the legend-revision page first. Today's date (2026-09-21) falls after the 2026-01-01 cutover, so the current table (`sec-hard-accrual`) is correct here — but the same question asked about a date in 2025 would need `hard-accrual-v2` instead, and the legend page warns explicitly that this is the case most likely to be gotten wrong. The three qualifiers (employment type, tenure band, site) each required a separate legend lookup to translate the plain-language description ("regular payroll", "five years", "Busan branch") into the row's index (E1, T3, L2) — none of this is guessable from the question wording alone, it's a literal lookup table. The row also carries a note about what happens if the carry-over or accrual figures are exceeded, which wasn't asked but is adjacent enough to flag if the person follows up.
