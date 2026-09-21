1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-v2/body
```

2. **Answer**
Supplier due diligence has three versions over time, and a claim dated in 2025 falls under the **second version** (in force 2024-07-01 to 2025-12-31), not the oldest version and not the current table (which only applies from 2026-01-01 onward). This middle version indexes checks by origin and value (two qualifiers), with the required-checks matrix:

| origin \ value | W1 | W2 | W3 | W4 |
|---|---|---|---|---|
| O1 | 30 | 31 | 32 | 33 |
| O2 | 34 | 35 | 36 | 37 |
| O3 | 38 | 39 | 40 | 41 |
| O4 | 42 | 43 | 44 | 45 |

All other elements (documents to collect, re-review interval) follow the original (oldest) supplier due diligence rule unchanged.

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (explains which of the three versions applies by date)
- /v1/nodes/hard-diligence-v2/body (the applicable version's content, in force 2024-07-01 to 2025-12-31)

4. **Notes**
The procurement region table lists both `sec-hard-diligence` (labeled "THE CURRENT SUPPLIER DUE DILIGENCE TABLE") and `hard-diligence-v2` (labeled "SUPERSEDED") side by side, with no obvious cue to check dates first — reaching straight for the "current" table would have been wrong here, since the claim is dated 2025 and the current table only applies from 2026-01-01. The `hard-diligence-legend-revision` file was the key: it explicitly warns that the oldest version says nothing about being superseded (so naive skimming of the oldest doc alone would look authoritative and complete), and that for 2025 specifically neither extreme (oldest nor current) is right — only the middle version. Without that legend page I'd likely have picked the current table by default. Did not need to consult `sec-supplier-due-diligence` (the "where to start" overview) or the oldest `supplier-due-diligence` page, since the legend page and the middle version's own body were sufficient and self-confirming (the v2 body cross-references both neighbors and their date boundaries).
