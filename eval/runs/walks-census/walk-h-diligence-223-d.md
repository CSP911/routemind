## Commands

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k4/body
```

## Answer

Yes, a site visit is required. The file is re-reviewed every 12 months.

(Also on this row, for context: screening score required 73, financial statements for the last two years.)

## Source

- /v1/nodes/hard-diligence-legend-revision/body — confirmed which of the three due-diligence table versions applies for today's date (2026-09-20 → current table)
- /v1/nodes/hard-diligence-row-origin-o3-value-w3-goods-k4/body — the row with the site-visit and re-review figures

## Notes

The supplier due diligence subject has three superseded/current versions (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`), and the legend page warns explicitly that the oldest version says nothing about being replaced — so grabbing the first plausible-looking row without checking the revision legend would have silently given 2024-era or pre-2024 figures. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-diligence`) was correct, but this was a real fork in the walk, not a formality — worth checking every time rather than assuming "current" is always right. Once in the current table, the row was addressed directly and unambiguously by the three qualifiers (O3/W3/K4), no legend lookups for the codes themselves were needed since the question already gave the codes rather than plain-language descriptions.
