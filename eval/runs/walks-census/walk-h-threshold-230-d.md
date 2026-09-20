1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m1/body

2. **Answer**
For category C3, amount V4, term M1 (current table, in force since 2026-01-01): the department head signs it off. Yes, other prices are required first — three competing quotes plus a written comparison. (Delegation limit for this row is 100044 thousand KRW; 11 working days to expect.)

3. **Source**
/v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m1/body
(confirmed via /v1/nodes/hard-threshold-legend-revision/body that this is the correct version for today's date, 2026-09-21)

4. **Notes**
The procurement area has three superseded versions of the approval-threshold table (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the oldest one gives no indication it was ever replaced. It would have been easy to grab the first threshold-looking table found without checking dates. I deliberately read the legend-revision page first to confirm which version covers 2026-09-21 before opening any row — the current table (`sec-hard-threshold`, in force from 2026-01-01) was the right one. The C3/V4/M1 codes given in the question matched a row address exactly, so no legend lookup for category/amount/term codes was needed — the row itself covered both parts of the question (signer and quote requirement) in one document.
