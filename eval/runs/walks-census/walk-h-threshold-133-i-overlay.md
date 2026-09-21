1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Consultant time, about 40 million won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table, in force since 2026-01-01 — need signer for ~40M won consulting/services spend" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold has three versions; need to confirm which applies and how to read the table" --member /v1/nodes/purchase-request "purchase request flow includes quotes requirement"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_33e495 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m4/body

2. **Answer**
Signs it off: the CFO. Competing quotes: yes — three, plus a written comparison. (Delegation limit for this row is 100,031 thousand KRW; expect 14 working days.)

This is the current table (in force from 2026-01-01, today's question is dated 2026-09-21), row for category C2 (a consultant's time), amount V4 (about 40 million won), term M4 (until we cancel it).

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" → C2)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "about 40 million won" → V4)
- /v1/nodes/hard-threshold-legend-term/body (mapped "until we cancel it" → M4)
- /v1/nodes/hard-threshold-legend-revision/body (confirmed current table applies for a 2026-09-21 question, not the superseded versions)
- /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m4/body (the answer row)

4. **Notes**
The procurement table lists two older threshold pages (`hard-threshold-v2`, superseded, and the even older `threshold-table` referenced only in the revision legend) right alongside the current one, with no obvious flag on which to use — the revision-legend page is what actually resolves this, and it explicitly warns that reaching for the newest is wrong for a pre-2026 date. Today's question is dated 2026-09-21, so the current table (`sec-hard-threshold`, three-qualifier rows) is right, but it would have been easy to skip that check and just grab the first "current" looking row.

The three qualifiers (category/amount/term) are each resolved through their own legend page rather than being obvious from the question's wording — "a consultant's time," "about 40 million won," and "until we cancel it" each had to be matched to the legend's exact phrasing (C2, V4, M4) rather than assumed. The overlay I created up front named `/v1/nodes/purchase-request` as a member on the theory that the quotes requirement might live in the general purchase-request flow rather than the threshold table itself — that member turned out to be unnecessary since the threshold row itself states the quote requirement directly ("three and a written comparison"), so I never had to open it.
