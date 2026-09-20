1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m3/body

2. Answer
For category C2, amount V3, term M3 (current table, in force from 2026-01-01): the division director signs it off. Yes, other prices are required first — three competing quotes. (For reference: delegation limit 20,026 thousand KRW; 10 working days to expect.)

3. Source
/v1/nodes/hard-threshold-legend-revision/body (confirmed which version applies for today's date, 2026-09-21)
/v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m3/body (the answer itself)

4. Notes
The procurement area lists three versions of the approval threshold table (oldest, a 2024-07-01–2025-12-31 middle version `hard-threshold-v2`, and the current `sec-hard-threshold` in force from 2026-01-01). The legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest version says nothing about being superseded — so it's easy to grab the wrong table if you don't check dates. Today (2026-09-21) falls after 2026-01-01, so the current table was correct, but this was a genuine branch point worth checking rather than assuming. The row for C2/V3/M3 existed directly under the current table's listing, so the amount/category/term legends were not needed since the codes were already given in the question.
