1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k3/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py overlay create --question "For origin O2, value W3, goods K3, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, indexed by origin/value/goods, in force 2026-01-01 onwards" --member /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k3/body "the exact row for O2/W3/K3" --member /v1/nodes/hard-diligence-legend-revision/body "confirms which of the three versions applies to a 2026-09-20 question"
./bench/rmcli.py overlay close --id ov_2026-09-20_ee9f43 --outcome answered --used /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k3/body /v1/nodes/hard-diligence-legend-revision/body

2. **Answer**: Yes, a site visit is required. The file is re-reviewed every 12 months.

3. **Source**:
/v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k3/body
/v1/nodes/hard-diligence-legend-revision/body

4. **Notes**: The procurement area table flagged up front that supplier due diligence has three superseded versions living side by side (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), so it would have been easy to grab an old row by mistake — the three tables are structurally similar (one/two/three qualifiers) but the row addresses for the current one are the only ones with the `origin-o2-value-w3-goods-k3` shape. I deliberately checked `hard-diligence-legend-revision` after reading the row to confirm today's date (2026-09-20) falls in the current table's "2026-01-01 onwards" range rather than assuming the newest table was automatically correct — the legend page itself warns that reaching for the newest is wrong for dates before 2026-01-01, which is exactly the mistake this walk was set up to invite. No ambiguity in the O2/W3/K3 codes themselves; the row was an exact, unique match once inside the current table.
