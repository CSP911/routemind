1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k1/body

2. **Answer**
No site visit is required. The file is re-reviewed every 36 months. (Screening score required: 46; financial statements not required.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions applies to today's date)
- /v1/nodes/hard-diligence-legend-origin/body (Stuttgart → origin O2)
- /v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
- /v1/nodes/hard-diligence-legend-goods/body (office consumables → goods K1)
- /v1/nodes/hard-diligence-row-origin-o2-value-w1-goods-k1/body (site visit: no; re-review interval: every 36 months)

4. **Notes**
The procurement area lists three eras of the supplier due diligence subject (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) without immediately saying which one is live. The legend-revision page is the only thing that resolves that, and it explicitly warns that the oldest page never marks itself as superseded and that grabbing the newest table on reflex is only safe for dates on or after 2026-01-01 — today (2026-09-20) qualifies, so `sec-hard-diligence` was correct, but this was a genuine branch point, not a formality. It would have been easy to skip that check and go straight to the current-looking table by name alone. Beyond that, the three-qualifier lookup (origin/value/goods) was mechanical once the three legend pages were read — each legend warns to record the mapping choice, but Stuttgart/eight million won/office consumables matched exact rows with no ambiguity or nearest-entry judgment needed.
