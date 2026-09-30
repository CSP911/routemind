1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Two-year contract, 5 years tenure, Busan branch: monthly accrual and January holding cap for leave?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site - directly answers monthly accrual rate"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l2/body
./bench/rmcli.py overlay add --id ov_2026-09-20_a15142 --address /v1/nodes/hard-accrual-legend-type/body --why "maps two-year contract to type E2"
./bench/rmcli.py overlay add --id ov_2026-09-20_a15142 --address /v1/nodes/hard-accrual-legend-tenure/body --why "maps five years service to tenure T3"
./bench/rmcli.py overlay add --id ov_2026-09-20_a15142 --address /v1/nodes/hard-accrual-legend-site/body --why "maps Busan branch to site L2"
./bench/rmcli.py overlay add --id ov_2026-09-20_a15142 --address /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l2/body --why "the matching row: E2/T3/L2 gives monthly accrual and carry-over limit"
./bench/rmcli.py overlay close --id ov_2026-09-20_a15142 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l2/body

2. **Answer**
Accrues 0.90 days of leave per month. The carry-over limit (the most you can still be holding at the start of the next year, i.e. in January) is 11 days.

3. **Source**
/v1/nodes/hard-accrual-legend-type/body (two-year contract → type E2)
/v1/nodes/hard-accrual-legend-tenure/body (five years → tenure T3)
/v1/nodes/hard-accrual-legend-site/body (Busan branch → site L2)
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l2/body (0.90 days/month accrual, 11-day carry-over limit)

4. **Notes**
The three qualifiers in the question (contract type, tenure, site) each had to be translated through a separate legend file before the right row (E2/T3/L2) could be picked out of the 64-row accrual table — none of the rows repeat the plain-language description, only the codes, so skipping any one legend would have made it impossible to pick the right row with confidence. "How much can I still be holding in January" is not phrased as "carry-over limit" anywhere in the source, so it would be easy to either miss that field or go looking for a separate document about year-end deadlines; the row itself only has one figure that fits the question ("Carry-over limit, days: 11"), which is what I used. I did not find any separate January-specific expiry rule elsewhere, but I also did not exhaustively check /v1/nodes/sec-days-that-decide-money, which could conceivably hold a related deadline — I'm treating the carry-over limit on the matching row as the direct answer since it's the one figure in the current, in-force (since 2026-01-01) table that answers "how much can still be held."
