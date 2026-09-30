## Commands

    ./bench/rmcli.py table
    ./bench/rmcli.py overlay create --question "Da Nang office-consumables supplier, KRW 300M: is a site visit required, and what is the re-review cycle for their vendor file?" --member /v1/regions/procurement "amount thresholds, supplier categories, and site-visit / periodic-review rules live under procurement"
    ./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
    ./bench/rmcli.py table /v1/nodes/sec-hard-diligence
    ./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
    ./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
    ./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
    ./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k1/body
    ./bench/rmcli.py overlay close --id ov_2026-09-20_5991e9 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k1/body

## Answer

Yes, a site visit is required. The file is re-reviewed every 12 months.

(Da Nang → origin O4, three hundred million won → value W3, "just office consumables" → goods K1; row O4/W3/K1 also requires a screening score of 86 and financial statements for the last two years, though those weren't asked.)

## Source

- /v1/nodes/hard-diligence-legend-revision/body — confirms the 2026-01-01-onward table is the one in force today (2026-09-20)
- /v1/nodes/hard-diligence-legend-origin/body — Da Nang → O4
- /v1/nodes/hard-diligence-legend-value/body — three hundred million won → W3
- /v1/nodes/hard-diligence-legend-goods/body — office consumables → K1
- /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k1/body — the answer: site visit yes, re-review every 12 months

## Notes

The near-miss here was the versioning, not the coding. Supplier due diligence has three superseded copies (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend page is explicit that "the oldest says nothing at all about having been replaced" — so grabbing the first hit for "supplier due diligence" without checking the revision legend would silently return stale rules. Today's date (2026-09-20) is safely inside the current bracket (2026-01-01 onward) so this wasn't a close call by date, but it was worth confirming rather than assuming the current table was current.

The three-way lookup (origin / value / goods) is otherwise mechanical once you find the three legend pages — each one is explicit that it is "the only place the mapping is written down" and to record the choice if the input isn't an exact match. All three inputs here (Da Nang, three hundred million won, office consumables) were exact matches in their legends, so no judgment calls were needed on the banding itself.
