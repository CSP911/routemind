1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k1/body
```

2. **Answer**
No site visit is required. The file (screening) gets re-reviewed every 36 months. (Screening score required: 62; financial statements not required.) This is under the current supplier due diligence table, in force from 2026-01-01, for origin O3 (a vendor in Austin), value W1 (eight million won), goods K1 (just office consumables) — all three qualifiers matched exactly, no nearest-entry judgment calls needed.

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which version's date range applies)
- /v1/nodes/hard-diligence-legend-origin/body (Austin → O3)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → W1)
- /v1/nodes/hard-diligence-legend-goods/body (office consumables → K1)
- /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k1/body (final answer)

4. **Notes**
The procurement table lists three versions of supplier due diligence side by side (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today (2026-09-20) falls inside the current table's range (2026-01-01 onward), so `sec-hard-diligence` was correct, but this is exactly the kind of question where grabbing the current-looking table without checking the revision legend first would silently give a right answer for the wrong reason — and would be wrong outright for a question dated in 2025. The three qualifiers (origin/value/goods) all mapped to exact, unambiguous legend entries, so no "nearest entry" fallback was needed here — that fallback logic exists in the legends but wasn't exercised.
