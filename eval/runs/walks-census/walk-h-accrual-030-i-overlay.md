1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Regular payroll, 9 years tenure, Seoul office: monthly leave accrual rate and max holding/cap in January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by employment type, tenure, site - directly answers accrual rate"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_d02a79 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l1/body

2. **Answer**:
- Accrues 0.64 days per month.
- Carry-over limit (max held) is 13 days — this is the cap that governs how much can still be held going into January.

3. **Source** (in order used):
- /v1/nodes/hard-accrual-legend-type/body
- /v1/nodes/hard-accrual-legend-tenure/body
- /v1/nodes/hard-accrual-legend-site/body
- /v1/nodes/hard-accrual-row-type-e1-tenure-t4-site-l1/body

4. **Notes**:
The table under /v1/regions/attendance lists three accrual pages — a legend-revision warning, a superseded v2 (2024-07-01 to 2025-12-31), and the current sec-hard-accrual (in force since 2026-01-01). With today's date of 2026-09-20/21, the current table is the right one, but it would be easy to grab the superseded v2 by mistake since both showed up in the same table listing with similar names.

The three plain-language qualifiers in the question ("regular payroll", "nine years", "Seoul office") don't map directly onto row addresses — each has its own legend file (type/tenure/site) that must be read first to translate them into the E/T/L codes used in the row filenames. Skipping the legends and guessing the code from the wording would risk picking the wrong row silently, since e.g. "nine years" isn't obviously "T4" without the tenure legend's banding table.

The question's two parts ("building up each month" and "how much can still be holding in January") both turn out to be single-row fields (monthly accrual rate and carry-over limit) rather than needing a separate lookup for the January cap — the row's "Carry-over limit" field answers the holding-cap half directly, with no separate year-end/January-specific rule found elsewhere in the accrual row or its legends.
