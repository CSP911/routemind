1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Regular payroll, 5 years tenure, fully remote/WFH: monthly leave accrual rate and max carryover holdable in January" --member /v1/regions/attendance "leave accrual and carryover rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_321298 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l4/body

2. **Answer**: Accrues 0.62 days per month. Carry-over limit into the new year is 13 days.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l4/body

4. **Notes**: This table has three superseded versions of the same subject (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`), and reaching for the current one by instinct would have been correct here only by luck — the legend-revision page explicitly warns that a 2025-dated question needs the middle version, not the newest. Today's date (2026-09-20) is past 2026-01-01, so `sec-hard-accrual` is right, but I checked the revision page first rather than assume. The three qualifiers (type/tenure/site) each needed their own legend to translate the plain-language question ("regular payroll", "five years", "fully from home") into codes (E1, T3, L4) — the row addresses are not guessable without reading all three legends first, matching the tool's "never construct one" rule. The row conflates "carry-over limit" with what the question calls "how much can still be holding in January" — I'm reading these as the same figure (the cap on balance carried into the new year), which seems right but the row doesn't use the word "January" itself, so this is an inference from context, not a verbatim match.
