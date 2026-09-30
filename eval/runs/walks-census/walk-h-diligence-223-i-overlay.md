## Commands

```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Vendor in Austin, 300M KRW, license: on-site visit required? review frequency?" --member /v1/regions/procurement "procurement threshold/vendor diligence table is most likely to cover site visits and review cadence for vendors"
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7179dc --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k4/body
```

## Answer

Yes, a site visit is required. The file is re-reviewed every 12 months.

(Full row for this case: screening score required 73, financial statements for the last two years, site visit yes, re-review interval every 12 months.)

## Source

- /v1/nodes/hard-diligence-legend-revision/body — established the current table (in force from 2026-01-01) is the right one to use for a question dated 2026-09-20
- /v1/nodes/hard-diligence-legend-origin/body — "a vendor in Austin" → origin O3
- /v1/nodes/hard-diligence-legend-value/body — "three hundred million won" → value W3
- /v1/nodes/hard-diligence-legend-goods/body — "a licence" → goods K4
- /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k4/body — the row itself: site visit and re-review interval

## Notes

- This subject has three superseding versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the oldest version carries no notice that it was ever replaced — the legend-revision page is the only thing that says so. Skipping straight to the newest-looking table without checking that page would have worked out fine here (today's date falls under the current version), but only by luck; for a 2025-dated question it would have been the wrong table and nothing on the old page would have warned me.
- The three qualifiers (origin, value, goods) are indexed only by their coded form (O3/W3/K4) and the mapping from plain language exists in exactly one place each — the three legend pages. The row addresses themselves give no hint which words map to which code, so skipping the legends and guessing at a row address would have been guessing blindly, not shortcutting.
- The overlay's "reached" notice on close (meaning these addresses were read but never formally added as overlay members) is just a bookkeeping quirk of not calling `overlay add` for each hop — it didn't affect the answer.
