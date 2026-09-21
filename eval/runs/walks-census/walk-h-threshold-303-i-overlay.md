1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Dinner with a client, about 700,000 won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/expense "client entertainment expense of ~700,000 won - need signature/approval threshold" --member /v1/regions/procurement "term is open-ended ('until we cancel') which may make this a contract subject to procurement approval threshold and competitive quote (other prices) requirements"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py overlay add --id ov_2026-09-21_f9ff64 --address /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m4/body --why "exact row: category C4 (dinner with a client), amount V1 (about 700,000 won), term M4 (until we cancel it)"
./bench/rmcli.py overlay add --id ov_2026-09-21_f9ff64 --address /v1/nodes/hard-threshold-legend-revision/body --why "check which threshold table version is in force for today's date 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_f9ff64 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m4/body

2. **Answer**
The department head signs it. No competing quotes ("other prices") are required — the row's Competing quotes field is "none." (Delegation limit for this row is 1,051 thousand KRW, well above the ~700,000 won figure; expect 5 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m4/body

4. **Notes**
"Until we cancel it" reads like odd phrasing for a one-off dinner, and it was tempting to treat this as a one-time expense (term M1) and stop at the expense region. But the term legend maps that exact phrase to M4 ("until we cancel it" = open-ended commitment), distinct from "just the once" (M1). The category legend also maps "dinner with a client" verbatim to C4 — so both the amount and the unusual term phrase are lookup keys into the threshold legends, not incidental color. Missing that would have produced the wrong row (a one-off C4/V1/M1 dinner likely has a different quote requirement). Also had to check hard-threshold-legend-revision to confirm which of the three threshold-table versions applies on 2026-09-21 — the current table (effective 2026-01-01 onward) is correct here, but the warning that "reaching for the newest is wrong for anything before 2026-01-01" made it worth verifying rather than assuming.
