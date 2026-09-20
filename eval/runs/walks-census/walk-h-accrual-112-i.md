1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l3/body

2. **Answer**
Accrues 0.84 days per month. Carry-over limit (the most that can still be held into January) is 9 days.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirms the 2026-01-01-onwards table is the one to use for today's date)
/v1/nodes/hard-accrual-legend-type/body (two-year contract → type E2)
/v1/nodes/hard-accrual-legend-tenure/body (been here two years → tenure T2)
/v1/nodes/hard-accrual-legend-site/body (Singapore entity → site L3)
/v1/nodes/hard-accrual-row-type-e2-tenure-t2-site-l3/body (0.84 days/month accrual, 9 days carry-over limit)

4. **Notes**
The attendance table lists three eras of the leave-accrual subject (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with an explicit warning that the newest is not always right — I checked the revision-legend page before picking a version rather than assuming "current" was correct, since today (2026-09-20) falls after the 2026-01-01 cutover this is the right table, but for a 2025-dated question it would have been `hard-accrual-v2` instead. The three qualifiers (type/tenure/site) each needed their own legend lookup — none of the row addresses can be built by guessing from the person's own words (e.g. "two-year contract" and "been here two years" both map to codes starting with different letters, E2 vs T2, easy to transpose if not careful). "How much can I still be holding in January" reads like a carry-over/cap question rather than an accrual-rate question; the row's "Carry-over limit" field answers it directly, so I did not need a separate document about year-end leave forfeiture or carry-over policy.
