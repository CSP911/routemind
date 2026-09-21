1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Singapore, regular payroll, 2 years tenure: monthly leave accrual rate and max carryover/holding into January" --member /v1/regions/attendance "leave accrual rates and carryover caps are attendance topics"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5918b1 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l3/body

2. **Answer**: You accrue 0.52 days of leave per month, and can hold (carry over) up to 9 days into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e1-tenure-t2-site-l3/body

4. **Notes**: The three qualifiers in the question ("regular payroll", "two years", "Singapore entity") map to codes only through three separate legend files (type E1, tenure T2, site L3) — none of this is guessable from the row address alone, and the legends explicitly warn they are "the only place the mapping is written down." The `sec-hard-accrual` table also carries a loud warning that leave accrual has THREE versions with overlapping-sounding date ranges (`leave-accrual`, `hard-accrual-v2` for 2024-07-01–2025-12-31, and the current one from 2026-01-01). It would be easy to grab the wrong version without checking today's date (2026-09-20/21) against the "in force from" line on the row itself — I confirmed the row I used states it's in force from 2026-01-01, which covers today. The row's "carry-over limit" field is what answers "how much can I still be holding in January" — the question's phrasing doesn't use the document's own term, so that connection has to be made explicitly rather than found by keyword match.
