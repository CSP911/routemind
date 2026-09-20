## Commands

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k3/body
```

## Answer

No, a site visit is not required. The file is re-reviewed every 24 months.

(Row detail: origin O3 / value W2 / goods K3 — screening score required 68, financial statements from last year, site visit "no", re-review interval "every 24 months".)

## Source

- `/v1/nodes/hard-diligence-legend-revision/body` (confirms which of the three diligence versions is current for today's date, 2026-09-20)
- `/v1/nodes/hard-diligence-legend-origin/body` (Austin → O3)
- `/v1/nodes/hard-diligence-legend-value/body` (sixty million won → W2)
- `/v1/nodes/hard-diligence-legend-goods/body` (people's time → K3)
- `/v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k3/body` (the answer)

## Notes

The three legend tables (origin, value, goods) matched the question's own wording almost verbatim — "a vendor in Austin," "sixty million won," "people's time" are literally the example rows in each legend, so there was no ambiguity in coding the row. The one place a wrong turn was possible: the procurement area lists three generations of the due-diligence table (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) at the same level, and the legend-revision page warns explicitly that grabbing the newest one is wrong for a question dated before 2026-01-01. Today's date (2026-09-20) falls inside the current version's range, so `sec-hard-diligence` was correct, but this is the kind of table where checking the revision legend before reading a row matters — it would have been easy to skip straight to the row lookup and never notice the versioning.
