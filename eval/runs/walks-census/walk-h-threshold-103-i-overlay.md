1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Consultant's time, ~700,000 won, until we cancel it: whose signature, and do I need other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term" --member /v1/nodes/purchase-request "how many quotes are needed" --member /v1/nodes/hard-threshold-legend-revision/body "warning about which threshold version applies to which dates"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_dbd7a3 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m4/body

2. **Answer**: The department head signs it off, and no competing quotes are required. This is category C2 (a consultant's time), amount band V1 (about 700,000 won, delegation limit 1,019 thousand KRW), term M4 (until we cancel it) — an open-ended commitment. Expect 5 working days.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirms today's date, 2026-09-20/21, falls under the current table in force from 2026-01-01, not an older version)
- /v1/nodes/hard-threshold-legend-category/body (maps "a consultant's time" → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (maps "about 700,000 won" → amount V1)
- /v1/nodes/hard-threshold-legend-term/body (maps "until we cancel it" → term M4)
- /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m4/body (the row itself: department head signs, no competing quotes, 5 working days)

4. **Notes**: The procurement table opened onto `/v1/nodes/sec-hard-threshold` and `/v1/nodes/approval-threshold` as two separate-looking tables for the same subject — the legend-revision warning made clear these are different eras (current vs. older two-qualifier version), not two live systems, so I stuck to the current one. The current threshold table isn't one document but a matrix keyed by three separate legends (category, amount, term) that each have to be resolved independently before the row address can even be constructed — easy to miss one and grab the wrong row. The phrase "until we cancel it" isn't obviously a "term" in the everyday sense (I first read it as asking about a cancellation policy), but the term legend's four options made clear it maps directly to M4 ("until we cancel it," an open-ended/no-fixed-end commitment) rather than being a separate question about cancellation rights. "Competing quotes: none" directly answers the "other prices first" half of the question — worth stating explicitly since it's easy to skim past in the row's table.
