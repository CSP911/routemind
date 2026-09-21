1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body

2. **Answer**
Supplier due diligence has been rewritten twice — three versions total:
- Version 1 (original): in force until 2024-07-01
- Version 2: in force 2024-07-01 to 2025-12-31
- Version 3 (current): in force from 2026-01-01 onwards

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (primary — gives the version count and all three date ranges)
- /v1/nodes/supplier-due-diligence/body (confirms the original version exists and carries no supersession notice itself, as the legend warns)

4. **Notes**
The procurement region's table listing was itself slightly misleading: it only surfaced two of the three due-diligence documents directly (hard-diligence-v2 and sec-hard-diligence), plus the legend-revision warning page — the original version's document (supplier-due-diligence) wasn't listed there at all and only turned up via the sec-supplier-due-diligence overview table. Without following that second table, I'd have undercounted at two versions instead of three. The legend page is explicit that the oldest version says nothing about being superseded, so if I'd only read supplier-due-diligence/body I would have wrongly treated it as still current — the legend page is the one that actually resolves the "how many times" and "which dates" question, and it was worth trusting over piecing dates together from the individual version pages.
