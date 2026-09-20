1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l4/body

2. **Answer**: For type E1, tenure T1, site L4 (current table, in force since 2026-01-01): accrues 0.46 days per month. The carry-over limit is 7 days — that is the most you can still be holding into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body (confirmed which version applies for today's date, 2026-09-20)
/v1/nodes/hard-accrual-row-type-e1-tenure-t1-site-l4/body (the figures)

4. **Notes**: The attendance area lists three separate versions of the leave-accrual subject (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with a dedicated legend-revision page warning that reaching for the newest is wrong for dates before 2026-01-01. Today (2026-09-20) falls under the current table, `sec-hard-accrual`, so no ambiguity here — but it would have been easy to skip the revision-legend check and just grab whatever table looked "current" by name. Since the question already gave the exact type/tenure/site codes (E1/T1/L4), there was no need to consult the separate site/tenure/type legends to translate a plain-language description into codes — the row address was unambiguous once the current table was opened.
