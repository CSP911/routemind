1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W3, goods K1, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force 2026-01-01, likely has origin/value/goods matrix with site visit and review frequency columns" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence table with different date ranges - need to confirm current version applies" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together, may clarify terms like site visit / review frequency"
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k1/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py overlay close --id ov_2026-09-20_5109d7 --outcome answered --used /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k1/body /v1/nodes/hard-diligence-legend-revision/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 12 months.

3. **Source**:
- /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k1/body (the O3/W3/K1 row itself: Site visit = yes, Re-review interval = every 12 months)
- /v1/nodes/hard-diligence-legend-revision/body (used to confirm today's date, 2026-09-20/21, falls in the "2026-01-01 onwards" range, so the three-qualifier current table `sec-hard-diligence` — and this row under it — is the right version, not `hard-diligence-v2` or the oldest `supplier-due-diligence`)

4. **Notes**: The main trap here is version confusion — procurement's due-diligence subject has three superseded tables (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) all still live, indexed by one, two, and three qualifiers respectively. Since the question gives three qualifiers (origin, value, goods) it already points at the current table, but I checked the legend-revision page anyway to be sure, since the warning explicitly says reaching for the newest is wrong for dates before 2026-01-01 — today isn't, so no issue, but it's the kind of thing that would silently give a wrong answer for a differently-dated question. Otherwise the walk was direct: the overlay's row-per-combination listing under sec-hard-diligence made the exact address (origin-o3-value-w3-goods-k1) obvious with no ambiguity.
