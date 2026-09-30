1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Dinner with a client, roughly 3 million won, locked in for three years: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "approval threshold by category, amount and term is the current table for this" --member /v1/nodes/purchase-request "how many quotes are needed before a purchase" --member /v1/nodes/hard-threshold-legend-revision/body "warning about which threshold version applies for 2026-09-20"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_2df824 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m3/body

2. **Answer**
The department head signs it off. Yes — two competing quotes are required. (Delegation limit for this row is 5,054 thousand KRW; 7 working days to expect.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m3/body

4. **Notes**
The opening table under /v1/regions/expense mentions "the entertainment cap," which looks like the obvious hit for "dinner with a client" — I nearly went there first. But that cap is about what the corporate card may spend per event, not about signature/approval chains for a locked-in multi-year commitment. The "locked in for three years" phrase is what tips this into procurement's approval-threshold table instead of a plain expense claim: it's not a one-off dinner reimbursement but a term commitment (e.g. a standing arrangement), so it's indexed by category/amount/term rather than by expense caps.
The threshold table itself is a three-axis matrix (category C1–C4 × amount V1–V4 × term M1–M4), and none of the individual row addresses hint at which axis values apply — you have to fetch the three legend files (category, amount, term) separately and map the question's plain-language description onto each axis before you know which of the 64 rows to read. Easy to guess wrong here without checking all three legends.
Also had to check the revision-legend file first: approval thresholds have three historical versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward), and only the last is current as of 2026-09-20, so reading the current `sec-hard-threshold` rows was correct — but that was a deliberate check, not an assumption.
