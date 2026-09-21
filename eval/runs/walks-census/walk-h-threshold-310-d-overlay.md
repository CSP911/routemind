1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C4, amount V2, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - since 2026-01-01" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold has three versions, need to check which applies"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_0cdfea --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m1/body

2. **Answer**:
The team lead signs it off. Yes — two competing quotes are required first. (Delegation limit for this row is 5,052 thousand KRW; expect 5 working days.)

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (established the current table applies, since no date was specified in the question and today is 2026-09-21)
/v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m1/body (the row with the actual figures)

4. **Notes**:
The question gives no date, and this table has three superseded versions covering different date ranges (until 2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward). The legend-revision page is explicit that reaching for the newest is wrong for anything dated before 2026-01-01, and that the oldest version says nothing about being replaced — so skipping that check would have been the easy way to go wrong on a stale-but-plausible-looking answer. Absent any date in the question, today's date (2026-09-21) puts it in the current table, `sec-hard-threshold`.

One procedural wrinkle: when I created the overlay I added `/v1/nodes/sec-hard-threshold` (the table) as a member rather than the specific row address, since the row addresses were only visible after opening that table. When I closed the overlay citing the row address, the tool flagged it as "reached = answered from somewhere the overlay never named" rather than a plain member hit. Not an error, just a reminder that adding a table as a member doesn't implicitly cover the rows printed inside it — worth adding the row itself as a member in future once it's known, before closing.
