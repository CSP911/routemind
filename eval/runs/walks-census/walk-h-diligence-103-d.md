1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k4/body

2. **Answer**: No site visit required. Re-review interval is every 36 months. (Also: screening score required 49, financial statements not required.)

3. **Source**:
/v1/nodes/hard-diligence-legend-revision/body (to confirm which of the three versions applies for today, 2026-09-20)
/v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k4/body (the answer)

4. **Notes**: The procurement table lists three separate due-diligence documents (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) with no obvious flag on which is current — the legend-revision page warns explicitly that "the oldest says nothing at all about having been replaced" and that reaching for the newest is wrong for dates before 2026-01-01. Since today is 2026-09-20, the current table (`sec-hard-diligence`) is correct, but this was the one place a careless walk could have grabbed the wrong version silently. The row address itself was guessable from the origin/value/goods codes and printed exactly as listed in the table, so no construction was needed — just confirmation it existed before reading.
