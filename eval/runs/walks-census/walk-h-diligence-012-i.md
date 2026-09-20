1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k3/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body

2. **Answer**: No, a site visit is not required. The file is re-reviewed every 24 months.
(This is for a Daejeon-based supplier, a contract worth sixty million won, for a "people's time" / labor-type purchase — origin O1, value W2, goods K3 in the current supplier due-diligence table, in force since 2026-01-01, which applies to today's date of 2026-09-20.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → O1)
- /v1/nodes/hard-diligence-legend-value/body (sixty million won → W2)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → K3)
- /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k3/body (site visit: no; re-review interval: every 24 months)
- /v1/nodes/hard-diligence-legend-revision/body (confirms the 2026-01-01 table is current for today's date)

4. **Notes**: The initial dead end was `supplier-due-diligence/body`, which reads like the main due-diligence page but only covers the generic sanctions/code-of-conduct/disqualification screen — it has no site-visit or re-review figures at all and doesn't mention value or origin banding. It would be easy to stop there and report "not found." The actual numbers live one level down, in the current hard-diligence table (`sec-hard-diligence`), which is keyed by three separate legend lookups (origin, value, goods) that have to be resolved individually before the row address can be built — the row addresses are entirely mechanical (`hard-diligence-row-origin-o1-value-w2-goods-k3`) and match the plain-language inputs cleanly once you have the three codes, so no interpolation was needed. The other trap flagged explicitly by the tool itself is the revision legend: there are three versions of this table (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and grabbing the newest without checking the date would be wrong for a 2025-dated question. For this question (dated today, 2026-09-20) the current table is correct, but that had to be verified rather than assumed.
