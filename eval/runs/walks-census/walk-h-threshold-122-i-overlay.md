1. Commands:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Consultant's fee ~12M KRW, 3-year contract: whose signature is needed, and are competing quotes required first?" --member /v1/regions/procurement "approval threshold and quote requirements by amount/term for procurement"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d3cc26 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m3/body

2. Answer:
The division director signs it off. Three competing quotes are required. (Delegation limit for this row: 20,026 thousand KRW; expect 10 working days.)

3. Source:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m3/body

4. Notes:
"A consultant's time" and "locked in for three years" map exactly to legend wording (category C2, term M3), so no ambiguity there. The amount, ~12 million won, matches "around 12 million won" (amount V3) closely rather than exactly — the legend explicitly says to take the nearest entry if not a literal match, so this was a safe pick, not a guess. The approval-threshold table warned of three historical versions (hard-threshold-legend-revision); I confirmed the row I used comes from the table marked "in force from 2026-01-01," which covers today's date (2026-09-21), so I did not need to open the legend-revision or superseded v2 page — but it would have been easy to grab a stale row without checking that "in force from" line first.
