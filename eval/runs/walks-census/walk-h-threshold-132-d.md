1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m3/body

2. **Answer**
For category C2, amount V4, term M3: the division director signs it off. Yes — three competing quotes plus a written comparison are required before approval. (Delegation limit for this row is 100,030 thousand KRW; expect 13 working days.)

3. **Source**
/v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m3/body

4. **Notes**
The procurement region listing flagged that the approval threshold has three versions (current, a 2024-07-01–2025-12-31 superseded one, and an older `threshold-table`), with a warning node (`hard-threshold-legend-revision`) calling this out explicitly. I did not open that legend node — the row I read states its own effective date ("In force from 2026-01-01") and today is 2026-09-21, so it's unambiguously the current row and I didn't need the revision legend to disambiguate. Worth flagging that if the question's date were near a boundary (e.g. 2025-12-31/2026-01-01), skipping that check would have been risky.

The row address was reachable directly from the sec-hard-threshold table by pattern-matching category/amount/term codes (c2, v4, m3) in the printed address — no need to open the amount/category/term legend files, since the question already gave codes rather than plain-language descriptions.
