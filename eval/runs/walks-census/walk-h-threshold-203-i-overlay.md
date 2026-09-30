1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, about 700,000 won, until we cancel it: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "amount+term based approval threshold by category, this sounds like a recurring/open-ended travel purchase" --member /v1/regions/expense "flights/hotels could be travel expense booking rules"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_44bb17 --outcome answered --used /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m4/body

2. **Answer**: The department head signs it off. No competing quotes are required (Competing quotes: none). Delegation limit for this row is 1,035 thousand KRW; expect 5 working days.

3. **Source**:
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m4/body

4. **Notes**: The question maps to three separate legend lookups before the actual row can be found: "flights and hotels" → category C3, "about 700,000 won" → amount V1, and "until we cancel it" → term M4 (an open-ended/no-fixed-end commitment, as opposed to M2 "renewing every year" or M3 "locked in for three years" — easy to misread "until we cancel it" as a yearly renewal if you don't read the term legend carefully). The current threshold table (sec-hard-threshold, in force from 2026-01-01) is the right one for today's date (2026-09-21); I did not need to consult the superseded v2/legend-revision versions, but their presence in the table listing is a trap for anyone who grabs a row without checking which version is current. The overlay's "reached" annotation on close indicates these leaf addresses weren't formally added as overlay members (only the two top-level region tables were) — the working set only tracked the coarse region-level choice, not each drill-down step.
