1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l3/body

2. **Answer**:
Accrual: 0.76 days per month.
Carry-over limit into the new year (what can still be held in January): 6 days.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l3/body

4. **Notes**:
The legend-revision page was the important gate: there are three versions of the leave accrual table (pre-2024-07-01, 2024-07-01–2025-12-31, and current from 2026-01-01), and it warns explicitly that reaching for the newest is wrong for a question dated before 2026-01-01. Today is 2026-09-20, so the current table (`sec-hard-accrual`) is correct here — but this is exactly the trap the page calls out, so it was worth checking rather than assuming.
All three qualifiers matched their legend entries exactly (two-year contract → E2, eight months → T1, Singapore entity → L3), so no "nearest entry above it" judgment call was needed — each legend also warns to fall back to the nearest listed value and record the choice if there isn't an exact match, which didn't apply here but is worth flagging as a place future questions could go wrong.
The row's "carry-over limit" field is what answers "how much can still be held in January" — the table doesn't use the word "January" anywhere, so this required inferring that carry-over limit = the cap on days held into the new year. Reasonably confident but not stated in those words.
