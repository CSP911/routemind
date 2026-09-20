1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m3/body

2. **Answer**:
For category C3, amount V3, term M3 (current table, in force from 2026-01-01, applies to today's date 2026-09-20): the division director signs it off. Yes — three competing quotes are required before approval. Delegation limit is 20,042 thousand KRW; 10 working days to expect.

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies for today's date)
- /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m3/body (the answer)

4. **Notes**:
The procurement region table lists both a current threshold table (`sec-hard-threshold`) and a superseded one (`hard-threshold-v2`), plus a "legend-revision" warning page saying there are actually THREE versions with overlapping validity windows, and that picking the newest is wrong for dates before 2026-01-01. It would have been easy to skip that check and just grab the current table, which happens to be correct here since today (2026-09-20) falls after 2026-01-01 — but the revision page makes clear this isn't safe to assume without checking the date. Also worth flagging: the question already gave the row codes (C3, V3, M3) directly, so I didn't need the amount/category/term legend pages to translate a plain-language description into codes — but those legends exist and would be necessary if the values weren't already given as codes.
