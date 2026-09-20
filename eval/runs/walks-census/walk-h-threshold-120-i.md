1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m1/body

2. **Answer**: The department head signs it off, and yes — three competing quotes are needed. (This falls within the row's delegation limit of 20,024 thousand KRW, so no escalation above the department head is triggered. Expect about 8 working days.)

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m1/body

4. **Notes**: The procurement table flags up front that the approval threshold has THREE versions with a legend-revision warning — easy to grab a superseded row (`hard-threshold-v2` or the older `threshold-table`) by mistake. I stuck to `sec-hard-threshold`, which states plainly it's the current table in force from 2026-01-01, covering today's date (2026-09-20/21), so I didn't need to open the revision-legend file itself. The three qualifiers (category, amount, term) are each resolved through a separate legend file rather than being obvious from the question's wording — "a consultant's time" → C2, "around 12 million won" → V3, "just the once" → M1 — and the row address is built by combining those three codes, which only works because the legends spell out the exact code strings to concatenate. Nothing else was ambiguous; the row itself directly answers both parts of the question (signer and quote requirement) in one document.
