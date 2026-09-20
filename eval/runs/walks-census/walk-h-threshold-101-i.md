1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m2/body

2. **Answer**
The team lead signs it off. No competing quotes are required. (Delegation limit for this row is 1,017 thousand KRW; expect 3 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m2/body

4. **Notes**
The procurement area warns up front that the approval threshold subject has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and that "the oldest says nothing at all about having been replaced" — so grabbing the first threshold table found without checking the legend-revision page would silently give a superseded answer. With today's date (2026-09-20/21) the current table (`sec-hard-threshold`) is the right one, but this was worth confirming rather than assuming "newest is always right," since the same page says that assumption is wrong for 2025-dated questions. Mapping the three qualifiers (category/amount/term) required reading all three legend files since none of the row files repeat the plain-English descriptions — "a consultant's time" → C2, "about 700,000 won" → V1, "renewing every year" → M2. The row itself directly answers both parts of the question (signer, quote requirement), so no cross-referencing with the approval-region table was needed.
