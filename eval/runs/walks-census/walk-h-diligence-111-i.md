## Commands

    ./bench/rmcli.py table
    ./bench/rmcli.py table /v1/regions/procurement
    ./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
    ./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
    ./bench/rmcli.py table /v1/nodes/sec-hard-diligence
    ./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
    ./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
    ./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
    ./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k2/body

## Answer

No site visit is required. The supplier's file is re-reviewed every 24 months.

(Full row, for context: screening score required 51, financial statements from last year.)

## Source

- /v1/nodes/hard-diligence-legend-revision/body — established that today (2026-09-20) falls under the current table, not the two superseded versions
- /v1/nodes/hard-diligence-legend-origin/body — Stuttgart → origin O2
- /v1/nodes/hard-diligence-legend-value/body — sixty million won → value W2
- /v1/nodes/hard-diligence-legend-goods/body — "something made to our spec" → goods K2
- /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k2/body — the row itself, holding the site-visit and re-review answers

## Notes

The one place this could have gone wrong is the version fork: supplier due diligence has three
successive versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the
legend-revision page is explicit that the oldest version never says it was replaced — reaching for
it without checking the date would silently give a superseded answer. Today's date (2026-09-20)
sits cleanly after 2026-01-01, so the current table applies; no ambiguity there, but it was worth
confirming explicitly rather than assuming "current" is always right.

Otherwise the walk was direct: three legends translate the plain-English facts (Stuttgart, 60M won,
made-to-spec goods) into the three qualifiers O2/W2/K2 with no fuzziness — each was an exact match
in its table, not a "nearest entry" fallback. The row itself answered both parts of the question
directly, with no need to cross-reference the vendor-performance-and-renewal page — "re-review
interval" on this row is the file-review cadence the question was asking about, not a separate
concept.
