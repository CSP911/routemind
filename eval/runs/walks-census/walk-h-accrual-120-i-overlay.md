1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "2-year contract, 5 years tenure, Seoul office: monthly accrual and max holding in January" --member /v1/nodes/sec-hard-accrual "current accrual table by employment type, tenure, site since 2026-01-01" --member /v1/nodes/annual-leave "entitlement and booking procedure, may cover carryover/holding cap"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0009a5 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l1/body

2. **Answer**:
You accrue 0.88 days of leave per month. The carry-over limit is 10 days — that is the most you can still be holding into January (any unapproved excess above that is settled at 10 days and not recoverable).

3. **Source**:
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l1/body

4. **Notes**:
The three qualifiers in the question (two-year contract, five years, Seoul office) don't map to row keys directly — each had to be translated through its own legend file (type/tenure/site) before the row address could be built. Easy place to go wrong: "two-year contract" superficially sounds like it could mean tenure ("been here two years"), but it's actually the employment-type legend ("on a two-year contract" → E1... no, → E2), while "been here five years" is the tenure legend (→ T3). Mixing those two up would have picked the wrong row silently, since every combination has a valid row. Also worth flagging: the "annual-leave"/"leave-accrual" table pulled into the working set turned out to be the superseded pre-2026 version and wasn't needed — the current table (sec-hard-accrual, in force since 2026-01-01) had everything, including the carry-over figure that answers the "holding in January" half of the question.
