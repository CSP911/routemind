## Commands

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Stuttgart firm, KRW 300 million contract, licence required: site visit needed? review/renewal frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, likely holds site visit and review frequency requirements by origin/value/goods" --member /v1/nodes/hard-diligence-legend-revision/body "warns there are three versions of due diligence rules - need to confirm which version applies to today's date 2026-09-21" --member /v1/nodes/sec-supplier-due-diligence "overview of how the due diligence pages fit together, may clarify site visit vs periodic review distinction"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_52ad73 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k4/body
```

## Answer

Yes, a site visit is required. The file is re-reviewed every 12 months.

(This is under the current supplier due-diligence table, in force from 2026-01-01: a firm in Stuttgart is origin O2, three hundred million won is value band W3, and a licence is goods category K4. For that row: screening score required 57, financial statements for the last two years, site visit yes, re-review interval every 12 months.)

## Source

- /v1/nodes/hard-diligence-legend-origin/body — maps "a firm in Stuttgart" to origin O2
- /v1/nodes/hard-diligence-legend-value/body — maps "three hundred million won" to value W3
- /v1/nodes/hard-diligence-legend-goods/body — maps "a licence" to goods K4
- /v1/nodes/hard-diligence-legend-revision/body — confirms which of the three due-diligence table versions is in force for today's date
- /v1/nodes/hard-diligence-row-origin-o2-value-w3-goods-k4/body — the row itself, with the site visit and re-review figures

## Notes

The question's three descriptors ("a firm in stuttgart", "three hundred million won", "a licence") are not literal table values — they are examples that each map through a separate legend page (origin, value, goods) to a coded qualifier (O2, W3, K4). Nothing in the procurement table names these legends directly; they only turn up once the overlay is opened on `/v1/regions/procurement`, which fans out into the full grid of due-diligence rows plus three unlabeled legend files. It would be easy to grab a row using the English wording directly (e.g. guessing "Stuttgart" sorts under a "Europe" origin) instead of reading the legend, which is exactly the trap the legend pages warn about ("This table is the only place the mapping is written down").

The bigger risk was version: `hard-diligence-legend-revision/body` is explicit that supplier due diligence has been rewritten three times (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and that the oldest version says nothing about being superseded — so silently reading the wrong version would look complete and consistent, not obviously wrong. Today's date (2026-09-20/21, both after 2026-01-01) puts this squarely in the current table (`sec-hard-diligence`, indexed by three qualifiers), matching the row read above. Had the question been dated in 2025, the correct answer would have come from the middle version (`hard-diligence-v2`, two qualifiers) instead, per the revision page's explicit warning against defaulting to "the newest."
