1. **Commands**:
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C2, amount V4, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - directly answers signature/who approves" --member /v1/nodes/purchase-request "purchase request flow including quotes needed - answers whether other prices (quotes) are required first"
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m2/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_c2b16d --address /v1/nodes/purchase-request --why "row itself states the quote requirement (three quotes + written comparison), no need for the general purchase-request flow page"
./bench/rmcli.py overlay close --id ov_2026-09-21_c2b16d --outcome answered --used /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m2/body
```

2. **Answer**: For category C2, amount V4, term M2: signs it off — the division director. Delegation limit is 100,029 thousand KRW. Yes, other prices are required first — three competing quotes and a written comparison. Working days to expect: 12. In force from 2026-01-01 (current version, still active as of today, 2026-09-21).

3. **Source**: `/v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m2/body`

4. **Notes**: The procurement area's table listed three prior versions of this same threshold table (`hard-threshold-v2`, and an older `threshold-table` referenced from within the row itself) plus a legend-revision warning page — easy to grab a superseded row by mistake. I stuck to `sec-hard-threshold`, which is explicitly labeled "THE CURRENT APPROVAL THRESHOLD TABLE, in force from 2026-01-01," and today's date (2026-09-21) falls inside that window, so no version confusion in the end. I initially also pulled in `/v1/nodes/purchase-request` expecting to need a separate quotes-count table, but the row I read already answered both halves of the question directly (signer and quote count) in one document, so that second member turned out to be unnecessary and I removed it before closing.
