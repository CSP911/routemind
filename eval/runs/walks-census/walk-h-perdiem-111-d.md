1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s2/body

2. **Answer**:
Lodging cap: 179 USD per night. Receipt threshold: 34 USD — above that amount you must keep the receipt.

3. **Source**:
/v1/nodes/hard-perdiem-legend-revision/body (confirmed which of the three per-diem versions is current for 2026-09-20)
/v1/nodes/hard-perdiem-row-grade-g2-band-b2-stay-s2/body (the figures)

4. **Notes**:
The expense area warns up front that overseas per-diem has three superseded-but-still-present versions (`overseas-rates`, `hard-perdiem-v2`, `sec-hard-perdiem`), and that the oldest never says it was replaced — so grabbing the first per-diem table found without checking the revision-legend page would silently give a stale answer. Today's date (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-perdiem` was the correct one. Since the question already supplied the exact codes (G2, B2, S2) rather than plain-language descriptions, the grade/band/stay legend files were not needed — the row address could be built straight from the table's printed rows. Only one figure could plausibly be "what to put on a hotel each night" — the lodging cap — and only one plausibly answers the receipt-threshold question, so there was no ambiguity once the correct row was open.
