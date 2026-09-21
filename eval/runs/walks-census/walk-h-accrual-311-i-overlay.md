1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "Partner firm employee, 2 years tenure, Busan branch: monthly leave accrual amount, and max leave holdable/carryover into January?" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site - since 2026-01-01" --member /v1/nodes/annual-leave "entitlement and booking procedure, may cover carryover cap" --member /v1/nodes/hard-accrual-legend-revision/body "warns which accrual version covers which dates"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l2/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_1c8b0f --address /v1/nodes/annual-leave --why "not needed once hard-accrual row for E4/T2/L2 answered both accrual rate and carry-over limit"
./bench/rmcli.py overlay close --id ov_2026-09-20_1c8b0f --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l2/body

2. **Answer**:
Accrues 1.46 days of leave per month. The carry-over limit — the most you can still be holding into January — is 8 days. (This row also notes 6 working days' notice is required to book leave, and that leave does not accrue during unpaid leave, though those weren't asked.)

3. **Source**:
- /v1/nodes/hard-accrual-legend-type/body (mapped "here from our partner firm" → type E4)
- /v1/nodes/hard-accrual-legend-tenure/body (mapped "been here two years" → tenure T2)
- /v1/nodes/hard-accrual-legend-site/body (mapped "at the Busan branch" → site L2)
- /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l2/body (the answer: 1.46 days/month accrual, 8-day carry-over limit, in force from 2026-01-01)

4. **Notes**:
The legend for employment type has a trap: "on a two-year contract" is a separate entry (type E2) from "been here two years" (a tenure value, T2). The question's "been here two years" is clearly tenure phrasing, not a contract-length claim, so I didn't let the coincidental "two-year" wording pull me toward E2. Getting this wrong would have picked the wrong row silently, since every (type, tenure, site) combination exists and returns a plausible-looking answer — there's no error to catch it.

Also had to actively rule out the two superseded accrual versions (hard-accrual-v2 for 2024-07-01–2025-12-31, and the original leave-accrual before that). Today's date (2026-09-20) falls under the current table (sec-hard-accrual, in force from 2026-01-01), which the row itself confirms in its footer, so no ambiguity there — but the table listing flags this as a common trap ("THREE versions with different..."), worth being deliberate about rather than grabbing the first accrual-looking row.
