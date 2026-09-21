1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C4, amount V2, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table, in force since 2026-01-01, likely holds signature-by-category/amount/term" --member /v1/nodes/hard-threshold-legend-revision "warns threshold has THREE versions with different date ranges - need to confirm which applies to today 2026-09-21" --member /v1/nodes/purchase-request "purchase request table may cover quote requirements (other prices first)"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m4/body
./bench/rmcli.py overlay remove --id ov_2026-09-21_382819 --address /v1/nodes/purchase-request --why "not needed - the threshold row itself states the quote count"
./bench/rmcli.py overlay close --id ov_2026-09-21_382819 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m4/body

2. **Answer**: For category C4, amount V2, term M4: the division director signs it off, and two competing quotes are required before the purchase (delegation limit 5,055 thousand KRW, 8 working days to expect).

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed today, 2026-09-21, falls under the current 2026-01-01-onwards version, not the two superseded ones)
- /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m4/body (the row itself: signature and quote count)

4. **Notes**: The procurement region page carries an explicit warning that the approval-threshold subject has three superseded/current versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and that the oldest version says nothing about being replaced — so grabbing the first plausible-looking table without checking the legend-revision page would have silently given a stale answer. Checking the revision legend first confirmed today's date maps to the current table (`sec-hard-threshold`), which is exactly the one indexed by three qualifiers (category/amount/term) matching the question. I also initially pulled in `/v1/nodes/purchase-request` on the assumption "other prices first" might need a separate quotes-policy document, but the threshold row itself already states the required number of competing quotes, so that member was removed as unused before closing.
