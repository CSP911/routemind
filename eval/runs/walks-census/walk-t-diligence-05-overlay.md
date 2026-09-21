1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In March 2025, what screening was required for an origin O2 supplier at contract value W2? Answer under the version of supplier due diligence that was in force on that date." --member /v1/regions/procurement "procurement table likely holds supplier due diligence rules by origin and contract value"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/hard-diligence-v2
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/sanctions-ownership-checks/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7adab2 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-v2/body

2. **Answer**: 35 (origin O2, value W2, from the supplier due diligence version in force 2024-07-01 to 2025-12-31).

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body (establishes that March 2025 falls under the second/middle version)
- /v1/nodes/hard-diligence-v2/body (the table itself, O2 row × W2 column = 35)

4. **Notes**: There are three versions of supplier due diligence (oldest, a 2024-07-01–2025-12-31 middle version, and a current one from 2026-01-01), and the legend-revision page explicitly warns that reaching for the newest or oldest is wrong for a 2025 date — the middle version (`hard-diligence-v2`) applies. I nearly stalled looking for a "legend" translating the table's numeric cells (30–45) into named checks, since the current version's table (`sec-hard-diligence`) does use named legends (origin/value/goods) and per-cell documents. The `hard-diligence-v2` page has no such legend — its table's header ("The checks required, by origin and value") is followed by a footer sentence that, read carelessly, seems to say the checks-required figures "followed the supplier due diligence rule unchanged," which looks self-contradictory against the table just given. Cross-checking the parallel `hard-threshold-v2` page clarified the pattern: its table is headed "Who signs it, by category and amount" but the cells hold plain KRW figures, not signer names — confirming these version-2 tables store the raw figure directly in the cell with no separate lookup needed, and the footer sentence only disclaims the *other*, unlisted attributes (documents to collect, re-review interval / quote count, etc.) as unchanged. So the correct read is: take the cell value directly — O2/W2 = 35 — rather than searching for a legend that doesn't exist for this version.
