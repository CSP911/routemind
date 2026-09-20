1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k3/body
```

2. **Answer**
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Also on file: screening score required 88, financial statements for the last two years — not asked but part of the same row.)

3. **Source**
`/v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k3/body` (the current supplier due diligence table, in force from 2026-01-01, reached via `/v1/regions/procurement` → `/v1/nodes/sec-hard-diligence`).

4. **Notes**
- `/v1/regions/procurement` lists several superseded diligence pages (`hard-diligence-v2`, and a `hard-diligence-legend-revision` warning about three versions with different dates) right alongside the current `sec-hard-diligence` table. It would be easy to grab the wrong version if you didn't notice the "THE CURRENT SUPPLIER DUE DILIGENCE TABLE, in force from 2026-01-01" label — today (2026-09-20) is safely inside that range, so the current table is correct, but the trap is real.
- The row document's O4/W3/K3 codes matched the question's O4/W3/K3 wording directly, so no legend lookup (origin/value/goods) was needed — but that's a coincidence of the question phrasing already using the table's own code names, not something to rely on in general.
- The row body ends with a generic "If the figures are exceeded" clause about unapproved excess being unrecoverable — this reads like boilerplate carried over from an expense/threshold-style template and has nothing to do with site visits or re-review cadence. Ignored it as irrelevant to the question asked.
