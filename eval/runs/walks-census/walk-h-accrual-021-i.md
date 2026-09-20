1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l2/body

2. **Answer**
You accrue 0.58 days of leave per month, and can carry over (hold) up to 11 days into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirms the current, 2026-01-01-onwards table applies to today's date)
/v1/nodes/hard-accrual-legend-type/body (regular payroll → type E1)
/v1/nodes/hard-accrual-legend-tenure/body (five years → tenure T3)
/v1/nodes/hard-accrual-legend-site/body (Busan branch → site L2)
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l2/body (0.58 days/month accrual, 11-day carry-over limit)

4. **Notes**
The attendance table listed three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with a warning that the newest is not always correct — the legend-revision page states a 2025-dated question would need the superseded `hard-accrual-v2` table, not the current one. Since today is 2026-09-20, the current `sec-hard-accrual` table (in force since 2026-01-01) was the right pick, but this was the easiest place to grab the wrong row without checking dates first.

The 64-row table is indexed only by three-letter/number codes (E/T/L), not by the plain-language terms in the question, so the three legend pages (type, tenure, site) had to be read before the correct row address could be identified. Skipping straight to a guessed row address (e.g. e1-t3-l2) would have violated the "never construct an address" rule even though it happens to be right — the legends were fetched to confirm the mapping rather than assumed.

"How much can I still be holding in January" reads as the carry-over limit (11 days) rather than the monthly accrual rate — the row's own field is literally called "Carry-over limit, days," so this mapped cleanly once the row was open.
