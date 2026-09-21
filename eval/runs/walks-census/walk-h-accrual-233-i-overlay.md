1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "3 days/week, 9 years tenure, fully remote: monthly leave accrual and max carryover holdable in January?" --member /v1/regions/attendance "leave accrual rate and carryover rules live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b06bc1 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l4/body

2. **Answer**
Accrues 1.34 days of leave per month. Can hold at most 16 days carried over into January (the carry-over limit).

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e3-tenure-t4-site-l4/body

4. **Notes**
The near-miss here was the accrual table's three revisions: `hard-accrual-v2` covers 2024-07-01 to 2025-12-31, and it would have been easy to grab that one out of habit or because it sorted earlier in a search. Checking `hard-accrual-legend-revision/body` first confirmed that as of today (2026-09-20/21) the current table `sec-hard-accrual`, in force from 2026-01-01, is the correct one — no legacy version needed.

The other place to go wrong was mapping the three free-text qualifiers to codes without checking the legends: "three days a week" maps to employment type E3 (not a fractional/part-time percentage), "nine years" lands exactly on tenure T4 ("been here nine years" is the T4 example verbatim, so no nearest-band judgment call was needed), and "fully from home" maps to site L4. All three were exact matches in their legends, so no approximation was required — a cleaner case than the legends' own "take the nearest entry" fallback suggests is typical.

"How much can I still be holding in January" reads like it could ask about a separate January-specific carryover/expiry rule, but the row's own "Carry-over limit, days" field (16) directly answers it — no additional January-dated document was needed.
