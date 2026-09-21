1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 300,000,000 contract for people's time (services): is an on-site visit required, and how often is the file reviewed again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force 2026-01-01 onward, by origin/value/goods" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together, may clarify on-site visit and review cadence" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of supplier due diligence; need to confirm correct version for today's date"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k3/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_a4aa0d --address /v1/nodes/sec-supplier-due-diligence --why "not needed once the current table and legends resolved the exact row"
./bench/rmcli.py overlay close --id ov_2026-09-20_a4aa0d --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k3/body
```

2. **Answer**
Yes, a site visit is required. The supplier's file is re-reviewed every 12 months.
(This is the current supplier due diligence table, in force since 2026-01-01, row: origin O2 / Stuttgart, value W3 / three hundred million won, goods K3 / people's time.)

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three versions of the supplier-due-diligence table applies to today's date, 2026-09-20/21)
- /v1/nodes/hard-diligence-legend-origin/body (Stuttgart → origin O2)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → value W3)
- /v1/nodes/hard-diligence-legend-goods/body (people's time → goods K3)
- /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k3/body (the row with the actual figures: site visit yes, re-review every 12 months)

4. **Notes**
Nothing here is derivable by guessing — the phrasing in the question ("a firm in Stuttgart," "three hundred million won," "people's time") is deliberately the exact wording used in the three legend tables (origin, value, goods), not a paraphrase, and each legend is the *only* place that mapping is written down. Skipping straight to a diligence row without reading the legends first would have meant either guessing the qualifiers or picking a row that looked plausible by name.

The one place I nearly went wrong: the version-legend page (`hard-diligence-legend-revision`) warns that supplier due diligence has three versions, and states explicitly that the oldest version says nothing about being superseded — so opening `supplier-due-diligence` (the un-suffixed, oldest address, which reads as the obvious/canonical name) would silently give an out-of-date answer with no clue on that page that it isn't current. Today's date (2026-09-20/21) falls after 2026-01-01, so the current table `sec-hard-diligence` / rows under `hard-diligence-row-*` is correct — but this only holds because I checked the date against the revision legend rather than assuming the newest-sounding address was right by default.

I initially added `/v1/nodes/sec-supplier-due-diligence` (the "where to start" overview of the four due-diligence pages) to the overlay as a hedge, expecting it might define what "site visit" or "re-review" mean generally. It turned out unnecessary once the specific row gave the figures directly, so I removed it before closing rather than leaving a stale member in the overlay.
