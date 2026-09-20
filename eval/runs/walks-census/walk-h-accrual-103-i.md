1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l4/body

2. **Answer**
Accrual: 0.78 days per month.
Carry-over limit into January: 7 days maximum.
(Qualifiers used: two-year contract → type E2; eight months of service → tenure T1; fully from home → site L4. Leave does not accrue during unpaid leave.)

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual versions applies to today's date)
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l4/body (the figures)

4. **Notes**
The attendance table lists three accrual-related entries (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with no obvious cue on which to use — grabbing the newest-looking one without checking would have been fine here since today (2026-09-20) is after 2026-01-01, but the legend-revision page explicitly warns that for a 2025-dated question the middle version applies, not the newest, so checking it was worth doing rather than assuming "current" is always right. The three qualifiers (type/tenure/site) are each in a separate legend file and none of the 64 accrual rows restate the plain-language description, so skipping any one legend would have made it impossible to pick the right row with confidence. "How much can I still be holding in January" maps to the row's "Carry-over limit" field — there was no separate January-specific rule, so I treated the general carry-over limit as the answer to that part of the question.
