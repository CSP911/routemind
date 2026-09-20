1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m4/body

2. **Answer**
For category C1, amount V3, term M4 (current table, in force from 2026-01-01): the division director signs it off. Yes — three competing quotes are required before this can go for signature. Delegation limit is 20,011 thousand KRW; expect 11 working days.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of three threshold table versions applies to today's date, 2026-09-20)
/v1/nodes/hard-threshold-row-category-c1-amount-v3-term-m4/body (the answer itself)

4. **Notes**
The procurement table's row for this warned of three superseding versions of the approval-threshold subject (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01–onwards), and explicitly said reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being replaced — so checking the legend page before reading a row was necessary, not optional. Today (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-threshold` was correct, but it would have been easy to skip the legend check and grab a superseded row without noticing anything was wrong, since the old versions don't flag themselves as outdated. The row itself gave both parts of the answer directly (signer + quotes-required) with no need to cross-reference the legend-amount/category/term pages, since the exact C1/V3/M4 row address was already listed in the table.
