1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k2/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body

2. Answer

No site visit is required. The file is re-reviewed every 24 months.

(Daejeon → origin O1, sixty million won → value W2, "something made to our spec" → goods K2, under the current supplier due diligence table in force from 2026-01-01, which covers today's date of 2026-09-20.)

3. Source

- /v1/nodes/hard-diligence-legend-origin/body (Daejeon → O1)
- /v1/nodes/hard-diligence-legend-value/body (sixty million won → W2)
- /v1/nodes/hard-diligence-legend-goods/body (something made to our spec → K2)
- /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k2/body (Site visit: no; Re-review interval: every 24 months)
- /v1/nodes/hard-diligence-legend-revision/body (confirms this current table is the right version for a 2026-09-20 question)

4. Notes

The procurement table listed several superseded pages alongside the current one (`hard-diligence-v2`, `supplier-due-diligence`, and the `hard-diligence-legend-revision` warning) right next to `sec-hard-diligence`, the current table — it would have been easy to grab the wrong version by picking the first plausible-looking "supplier due diligence" row instead of the one explicitly marked current. I deliberately checked `hard-diligence-legend-revision` at the end to confirm 2026-09-20 falls under the 2026-01-01-onwards version I'd already used, rather than assuming. The three legend pages (origin/value/goods) were essential and non-obvious — the row addresses are built from codes (O1/W2/K2) that only exist in those legend tables, not from the plain-language terms in the question, so skipping any one of them would have made it impossible to construct the correct row address.
