1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Supplier in Da Nang, 300M KRW, custom-spec item: site visit required? review/reassessment frequency?" --member /v1/regions/procurement "procurement threshold/approval and supplier vetting rules likely live here"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_0fba71 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k2/body
```

2. **Answer**
Yes, a site visit is required. The supplier's file is re-reviewed every 12 months.
(Full row also specifies: screening score required 87, financial statements for the last two years — not asked for, included for completeness.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence versions applies to today's date)
- /v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → value W3)
- /v1/nodes/hard-diligence-legend-goods/body ("something made to our spec" → goods K2)
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k2/body (the answer: site visit yes, re-review every 12 months)

4. **Notes**
- The procurement region table's blurb only advertises approval thresholds ("how far up this amount has to be approved"), not supplier diligence — the diligence table only surfaced once the overlay opened. Worth remembering the region descriptions undersell what's inside.
- There's a live trap here: three separate versions of this due-diligence table exist (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and the oldest version says nothing about being superseded — it would look authoritative to anyone who found it first. The `hard-diligence-legend-revision` page exists specifically to catch this, and I read it before touching any row. Today's date (2026-09-20) falls in the current-version window (`sec-hard-diligence`, from 2026-01-01), so that's the one used — but a question dated anytime in 2025 would need `hard-diligence-v2` instead, and one before mid-2024 the oldest, unlabeled version.
- The three qualifiers (origin/value/goods) each have their own legend and must be read in full — the mapping is stated as "the only place... written down" and rows don't repeat the human-readable side, so guessing the code from the row name alone would risk misfiling the case (e.g. confusing "made to our spec" with a licence or straight goods).
- The overlay `close` command reported all five addresses I used as "reached" rather than the addresses I'd originally listed as overlay members — because I only ever added `/v1/regions/procurement` as a member and then drilled down freely via `table`/`read` rather than adding each address to the overlay with `add`. Functionally harmless here (the tool still recorded them), but worth noting the overlay's member list didn't end up reflecting the real path taken.
