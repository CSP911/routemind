## Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k4/body

## Answer

Yes, a site visit is required. The file is re-reviewed every 12 months.
(Also on this row, not asked but part of the same entry: screening score required is 57, and financial statements for the last two years must be collected.)

## Source

- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions applies to today, 2026-09-20 — the current one)
- /v1/nodes/hard-diligence-legend-origin/body (Stuttgart → origin O2)
- /v1/nodes/hard-diligence-legend-value/body (three hundred million won → value W3)
- /v1/nodes/hard-diligence-legend-goods/body (a licence → goods K4)
- /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k4/body (the row itself: site visit yes, re-review every 12 months)

## Notes

- The procurement region table warned up front that supplier due diligence has three superseded versions ("older pages on both subjects are still here and are superseded"), so I deliberately read the legend-revision page before touching any actual table. That page explicitly calls out 2025-dated questions as the trap case — reaching for the newest table there would be wrong. Today's date (2026-09-20) falls cleanly in the "2026-01-01 onwards" band, so `sec-hard-diligence` was the correct table, but I would have gotten this wrong without checking, since the naming of the superseded pages (`hard-diligence-v2`, plain `supplier-due-diligence`) gives no hint from the table listing alone about which dates they cover.
- The 64-row current table gave no shortcut to the right row — it's indexed by three separate qualifier codes (origin/value/goods) each requiring its own legend lookup. Easy to get impatient and guess a row address directly; the instructions explicitly forbid constructing addresses, and doing so here would likely have picked the wrong row since the codes (O2/W3/K4) aren't guessable from the plain-language question.
- The value legend maps "three hundred million won" exactly to W3 — no rounding or nearest-band judgment needed, which was a relief since the legend text warns to "take the nearest entry" if the value isn't listed exactly.
- Nothing about "licence" was ambiguous once I saw the goods legend — it's a literal, exact match to K4 ("a licence").
