## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Consultant time, ~3M won, locked in for 3 years: whose signature, and do I need other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category/amount/term, in force since 2026-01-01" --member /v1/nodes/purchase-request "purchase request process incl. how many quotes needed" --member /v1/nodes/hard-threshold-legend-revision/body "warning about three versions of threshold table, need to check which applies"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_91f2b6 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m3/body

## Answer
The department head signs it off. Yes — two competing quotes are required before the purchase. (Delegation limit for this row is 5,022 thousand KRW; expect 7 working days.)

## Source
- /v1/nodes/hard-threshold-legend-revision/body (confirms today's date, 2026-09-21, falls under the current table, not the two superseded ones)
- /v1/nodes/hard-threshold-legend-category/body (a consultant's time → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (roughly 3 million won → amount V2)
- /v1/nodes/hard-threshold-legend-term/body (locked in for three years → term M3)
- /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m3/body (the row itself: department head signs, two competing quotes)

## Notes
The procurement table lists both an old `approval-threshold` table (under purchase-request) and the current three-qualifier `sec-hard-threshold` table, plus two explicitly superseded versions (`threshold-table`, `hard-threshold-v2`) — easy to grab the wrong one if you don't stop at the revision-legend warning first. That warning page was the thing that kept me from just assuming "newest is right" without checking the date; it explicitly calls out that a 2025-dated question would need the *middle* version, so I made sure to actually confirm 2026-09-21 falls in the current window rather than assuming. The row itself is only reachable by decoding all three qualifiers (category/amount/term) through separate legend pages first — the row addresses give no hint which of C1–C4, V1–V4, M1–M4 apply without them, so skipping any one of the three legends would have produced a confidently wrong row.
