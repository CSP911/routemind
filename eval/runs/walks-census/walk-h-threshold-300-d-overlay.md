1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C4, amount V1, term M1, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term lives here"
./bench/rmcli.py overlay remove --id ov_2026-09-21_141573 --address /v1/nodes/contract-custody --why "not about approval thresholds"
./bench/rmcli.py overlay remove --id ov_2026-09-21_141573 --address /v1/nodes/ga-desk --why "not about approval thresholds"
./bench/rmcli.py overlay remove --id ov_2026-09-21_141573 --address /v1/nodes/hard-diligence-legend-revision/body --why "diligence not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_141573 --address /v1/nodes/hard-diligence-v2/body --why "diligence not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_141573 --address /v1/nodes/sec-contract-terms-the-company-insists-on --why "not about approval thresholds"
./bench/rmcli.py overlay remove --id ov_2026-09-21_141573 --address /v1/nodes/sec-hard-diligence --why "diligence not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_141573 --address /v1/nodes/sec-receiving-and-inspection --why "not about approval thresholds"
./bench/rmcli.py overlay remove --id ov_2026-09-21_141573 --address /v1/nodes/sec-supplier-due-diligence --why "diligence not threshold"
./bench/rmcli.py overlay remove --id ov_2026-09-21_141573 --address /v1/nodes/sec-vendor-performance-and-renewal --why "not about approval thresholds"
./bench/rmcli.py overlay remove --id ov_2026-09-21_141573 --address /v1/nodes/vendor --why "not about approval thresholds"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_141573 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m1/body

2. **Answer**:
The team lead signs it off. No competing quotes are required (Competing quotes: none). Delegation limit for this row is 1,048 thousand KRW, working days to expect: 2. This is the current table, in force from 2026-01-01, which applies to today's date (2026-09-21).

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed the current, 2026-01-01-onward version applies to today's date, not the two older versions)
- /v1/nodes/sec-hard-threshold (table listing, located the exact row for category C4, amount V1, term M1)
- /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m1/body (the row itself — signer and quote requirement)

4. **Notes**:
The overlay's `remove` calls all failed with 404 "not in this overlay" — the create step apparently only registered the one explicit `--member` (the procurement region), not the rest of the rows the region table happened to print afterward, so trying to prune those rows out of the overlay was a no-op that just produced ten error lines. Worth knowing: adding a table doesn't auto-populate the overlay with everything it prints; only explicit `--member`/`add` entries count as members. It didn't block finding the answer since I could still read addresses directly, but the working set never actually got narrowed as instructed, and the overlay `close` step flagged the addresses I did use as "reached" rather than "used from the working set" for the same reason.

The one place this question could have gone wrong is the three-version trap on approval-threshold documents: there's an old `threshold-table`, a superseded `hard-threshold-v2` (2024-07-01 to 2025-12-31), and the current `sec-hard-threshold` (2026-01-01 onward). Today's date (2026-09-21) falls under the current table, so `sec-hard-threshold` was correct, but I checked the legend-revision page explicitly before trusting that rather than assuming "current" was right by default — the legend page warns that reaching for the newest is wrong for dates before 2026-01-01, which is exactly the mistake this row structure is designed to invite.
