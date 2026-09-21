1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "A couple of laptops, about 40 million won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by amount/category for a one-time equipment purchase"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_8d8741 --outcome answered --used /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m1/body

2. **Answer**: The department head signs it off. Yes — three competing quotes and a written comparison are required before it can go through. (Delegation limit for this row is 100,012 thousand KRW, i.e. about 100M won, so the 40M won purchase is within the department head's authority; expect about 11 working days.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-category/body
- /v1/nodes/hard-threshold-legend-amount/body
- /v1/nodes/hard-threshold-legend-term/body
- /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m1/body

4. **Notes**: "A couple of laptops" maps straight to category C1 in the legend ("a couple of laptops" is the literal example given), "about 40 million won" is the literal example for amount V4, and "just the once" is the literal example for term M1 — all three legends happen to use almost the exact wording from the question, so there was little ambiguity in picking the row. The one place to be careful: the threshold table has three historical versions (a legend-revision warning flags this), and `/v1/regions/procurement` originally surfaced both `hard-threshold-v2` (superseded, 2024-07-01 to 2025-12-31) and `sec-hard-threshold` (current, in force from 2026-01-01) side by side in the same listing. Today's date (2026-09-21) falls under the current version, so I went straight to `sec-hard-threshold` and didn't need to open the superseded one or the revision legend — but it would be easy to grab the wrong version's row if you didn't check the in-force dates against today's date first.
