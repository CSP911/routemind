1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C3, amount V3, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table by category, amount, term - matches C3/V3/M3 directly" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold has three versions, need to confirm which is current" --member /v1/nodes/purchase-request "may cover quotes required before approval"
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m3/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d6392c --outcome answered --used /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m3/body /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**:
The division director signs it off. Yes — three competing quotes are required before approval. (Delegation limit for this row is 20,042 thousand KRW; working days to expect: 10.)

3. **Source**:
- /v1/nodes/hard-threshold-row-category-c3-amount-v3-term-m3/body (signature, quotes required, delegation limit)
- /v1/nodes/hard-threshold-legend-revision/body (confirms this row's table, `sec-hard-threshold`, is the current version in force from 2026-01-01, appropriate for today's date)

4. **Notes**:
The procurement region table lists three separate threshold pages (`hard-threshold-v2`, a legend-revision warning, and the current `sec-hard-threshold`) plus an older `approval-threshold` table nested under `purchase-request`. The legend-revision page is explicit that the subject has been written three times and "reaching for the newest is wrong for anything before 2026-01-01" — a real trap if the question had specified an older date instead of using today's. Since no date was specified in the question, today's date (2026-09-20/21) applies and the current table is correct, but I checked the revision-legend page deliberately rather than assuming. Opening `/v1/regions/procurement` surfaced the exact row address directly (`hard-threshold-row-category-c3-amount-v3-term-m3`) without needing to open the `sec-hard-threshold` table itself, so I read the row straight away — the overlay tool flagged this row as "reached" rather than "member" since I never explicitly added it, which is harmless but worth noting for future walks: adding the parent table as a member doesn't auto-register its child rows as members.
