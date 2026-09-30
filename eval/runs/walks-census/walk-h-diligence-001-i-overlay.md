1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Company in Daejeon, 8 million won, custom-made to spec: must we visit their premises, and how often is their file reviewed again?" --member /v1/regions/procurement "custom/spec order, amount threshold, and vendor site visit + review cadence sound like procurement/vendor management topics"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_47886a --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k2/body

2. **Answer**
No site visit is required. The file is re-reviewed every 36 months.
(Row: origin O1 = Daejeon, value W1 = eight million won, goods K2 = something made to our spec, screening score required 31, financial statements not required.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed current table applies: today, 2026-09-20, falls in the 2026-01-01-onwards version)
/v1/nodes/hard-diligence-legend-origin/body (Daejeon → O1)
/v1/nodes/hard-diligence-legend-value/body (eight million won → W1)
/v1/nodes/hard-diligence-legend-goods/body (something made to our spec → K2)
/v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k2/body (answer: site visit no, re-review every 36 months)

4. **Notes**
The main trap here was the due-diligence subject having three superseded-but-not-marked-superseded versions — the legend page explicitly warns that the oldest version "says nothing at all about having been replaced," so reaching for `supplier-due-diligence` (the original, unqualified address) without checking the revision legend first would silently give the wrong rules. Today's date (2026-09-20) put this squarely in the current table (`sec-hard-diligence`, in force from 2026-01-01), so no ambiguity in the end, but a 2025-dated question would have needed the middle version (`hard-diligence-v2`) instead — worth being deliberate about every time rather than assuming "current" is always right.
The other easy slip: all three qualifiers (origin, value, goods) happened to map exactly onto listed legend entries (Daejeon = O1, 8,000,000 won = W1, "made to our spec" = K2), so no nearest-entry judgment call was needed here — but the legends' "take the nearest entry above it" fallback language means that won't always be true, and it's worth checking each qualifier against its legend individually rather than pattern-matching from memory.
