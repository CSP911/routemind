1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C4, amount V3, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term - matches C4/V3/M1 directly"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_dd1213 --outcome answered --used /v1/regions/procurement /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m1/body

2. **Answer**: The department head signs it off. Yes — three competing quotes are required first. (Delegation limit for this row: 20056 thousand KRW; expect 8 working days.)

3. **Source**:
- /v1/regions/procurement (routed to the current threshold table)
- /v1/nodes/sec-hard-threshold (confirmed this is the current table, in force from 2026-01-01, and located the exact row)
- /v1/nodes/hard-threshold-row-category-c4-amount-v3-term-m1/body (the row itself — signer and quote count)

4. **Notes**: The procurement region table also surfaced two older/legend nodes for this same subject — `hard-threshold-v2` (marked SUPERSEDED, in force 2024-07-01 to 2025-12-31) and `hard-threshold-legend-revision` (a warning that approval threshold has three versions). It would have been easy to grab `hard-threshold-v2` by mistake since it sat right next to the current one in the listing with a similar name. I didn't open either — `sec-hard-threshold` itself states it is "THE CURRENT APPROVAL THRESHOLD TABLE, in force from 2026-01-01," and today's date (2026-09-21) falls inside that window, so I went straight to the C4/V3/M1 row from the current table's own index rather than checking the superseded version or the legend page. No ambiguity in the row itself — it names the signer, the quote count, and the delegation limit directly.
