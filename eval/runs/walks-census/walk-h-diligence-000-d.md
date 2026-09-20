## Commands

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k1/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
```

## Answer

No site visit is required. The file is re-reviewed every 36 months.
(Screening score required: 30; financial statements not required — noted for context but not asked.)

## Source

- /v1/nodes/hard-diligence-row-origin-o1-value-w1-goods-k1/body (primary answer: site visit = no, re-review interval = every 36 months)
- /v1/nodes/hard-diligence-legend-revision/body (confirms today, 2026-09-20, falls under the current 2026-01-01-onward version, not the two superseded ones)

## Notes

This subject has three superseded versions of the same table (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the table listing flags this loudly with a WARNING before you even open a row. The near-miss here: it would be easy to grab the first plausible-looking row address and answer without checking which version is actually in force. I checked `hard-diligence-legend-revision` explicitly — today's date (2026-09-20) is after 2026-01-01, so the current three-qualifier table (`sec-hard-diligence`) is correct, not the older two-qualifier `hard-diligence-v2`. Also worth noting: the row address itself (`hard-diligence-row-origin-o1-value-w1-goods-k1`) matched O1/W1/K1 directly and exactly as printed in the table listing, so no legend lookup for origin/value/goods codes was needed here — the question already used the codes verbatim.
