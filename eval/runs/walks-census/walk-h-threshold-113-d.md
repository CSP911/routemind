1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m4/body
```

2. **Answer**
For category C2, amount V2, term M4 (current table, in force from 2026-01-01, delegation limit 5023 thousand KRW): the division director signs it off, and yes — two competing quotes are required before proceeding. Working days to expect: 8.

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions applies to today's date)
- /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m4/body (the answer)

4. **Notes**
The procurement region listing flagged up front that the approval-threshold subject has three superseded versions living side by side (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and that the oldest one says nothing about having been replaced — so grabbing the first plausible-looking row without checking the legend-revision page would have silently returned stale (pre-2024-07-01 or 2024-07-01–2025-12-31) signer/quote rules instead of the current ones. Checked the revision legend before reading any row; today (2026-09-21) falls after 2026-01-01, so the current table `sec-hard-threshold` was correct. Once inside the current table, the row address matching C2/V2/M4 was printed directly by the table listing, so no further legend lookups (for what counts as C2, V2, or M4) were needed since the question already gave the codes directly.
