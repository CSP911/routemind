1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m3/body

2. **Answer**
The division director signs it off. Yes, three competing quotes are required first. (Delegation limit for this row is 20,026 thousand KRW; expect 10 working days.)

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "~12 million won" → amount V3)
- /v1/nodes/hard-threshold-legend-term/body (mapped "locked in for three years" → term M3)
- /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m3/body (the row itself: signer, quote count)

4. **Notes**
The procurement area warns up front that the approval-threshold subject has three versions (a current table since 2026-01-01, a superseded v2 for 2024-07-01–2025-12-31, and an older `threshold-table`), and there's a dedicated `hard-threshold-legend-revision` page just to sort out which dates go with which. Today is 2026-09-20/21, safely inside the current table's validity, so I went straight to `sec-hard-threshold` without opening the revision-legend or either superseded version — but it would have been easy to grab a stale row by address-guessing or by reading the wrong `hard-threshold-v2` entry, since the row addresses for the old and current tables look almost identical apart from which parent table lists them. The three legends (category/amount/term) are deliberately fuzzy in wording ("a consultant's time", "around 12 million won", "locked in for three years") and only make sense once you realize the row address is literally built from the three codes they hand you (c2/v3/m3) — nothing else in the table hints at that structure until you've read at least one legend.
