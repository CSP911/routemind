## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k4/body

## Answer
Yes, a site visit is required. The file is re-reviewed every 12 months.
(Screening score required: 73; financial statements: last two years — supporting context, not asked for.)

## Source
/v1/nodes/hard-diligence-legend-revision/body (confirms current table applies for 2026-09-20)
/v1/nodes/hard-diligence-legend-origin/body (Austin → O3)
/v1/nodes/hard-diligence-legend-value/body (300 million won → W3)
/v1/nodes/hard-diligence-legend-goods/body (a licence → K4)
/v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k4/body (final answer: site visit yes, re-review every 12 months)

## Notes
- The due-diligence subject has three superseded versions in place over time; the legend-revision page is explicit that reaching for the newest table is wrong for pre-2026 dates. Today's date (2026-09-20) falls cleanly in the "2026-01-01 onwards" band for `sec-hard-diligence`, so no ambiguity there, but skipping that check would have been the easy mistake to make.
- The three qualifiers (origin, value, goods) each map through a dedicated legend page rather than being guessable from the question's wording — "a vendor in Austin" isn't obviously "O3" and "a licence" isn't obviously "K4" without reading the legend tables verbatim. Guessing codes instead of reading the legends would risk landing on the wrong row silently, since all 64 rows look structurally identical.
- 300 million won hit an exact band boundary (W3) rather than needing "nearest entry above," so no rounding judgment call was needed here — worth flagging since the legend text implies that's sometimes required.
- Did not need to open `/v1/nodes/vendor` or `/v1/nodes/sec-vendor-performance-and-renewal` — the row itself already gave both answers (site visit + re-review interval), so no need to cross-reference the vendor-performance page for renewal cadence.
