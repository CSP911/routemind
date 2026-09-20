## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k3/body

## Answer
No site visit required. The file is re-reviewed every 24 months.

(Row: origin O2 = "a firm in Stuttgart", value W2 = "sixty million won", goods K3 = "people's time". Screening score required: 52; financial statements: last year — given for context, not asked.)

## Source
- /v1/nodes/hard-diligence-legend-revision/body (confirmed today's date, 2026-09-20, falls under the current version)
- /v1/nodes/hard-diligence-legend-origin/body
- /v1/nodes/hard-diligence-legend-value/body
- /v1/nodes/hard-diligence-legend-goods/body
- /v1/nodes/hard-diligence-row-origin-o2-value-w2-goods-k3/body (final answer)

## Notes
Two places this could have gone wrong:

1. **Version trap.** `/v1/regions/procurement` surfaces both the current due-diligence table (`sec-hard-diligence`) and a superseded one (`hard-diligence-v2`), plus a legend page warning there are three versions total and that a naive "grab the newest" reflex is only safe from 2026-01-01 onward. Today's date (2026-09-20) is after that cutover, so the current table is correct here — but the warning made clear this is a genuine trap for any question dated in 2025, where the middle version would apply instead.

2. **A dead-end detour.** The `sec-supplier-due-diligence` overview page describes "four pages" and one of the addresses it lists (`/v1/nodes/supplier-due-diligence/body`) turned out to be the *oldest, pre-2024-07-01* version of the due-diligence doc (per the legend, that address is literally the superseded original) — it has no site-visit or re-review-interval fields at all, just the old three-checks/sanctions narrative. I read it fully before recognizing it was a narrative/legacy page, not the current indexed table, and backed out to the row-lookup table (`sec-hard-diligence`) instead. Worth flagging: the "fourth page ... re-run rather than one-off" line in the overview never resolved to an obviously-matching address among the four listed — it may be loosely describing this same old page's suspension/re-check language rather than a distinct current ongoing-review page. It didn't matter for this answer since the real re-review figure lives directly on the matched row, but it's a soft spot in how that overview cross-references its own children.

No ambiguity in the three qualifier lookups themselves: "sixty million won" and "people's time" both hit exact legend rows (W2, K3) rather than needing the "nearest entry" fallback, and "a firm in Stuttgart" is an exact match for O2's example wording.
