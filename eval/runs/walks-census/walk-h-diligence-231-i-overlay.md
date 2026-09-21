## Commands

```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Austin vendor, custom-spec order (700M KRW): site visit required? file review cadence?" --member /v1/regions/procurement "procurement region covers vendor approval thresholds, site visits, and review cadence for custom-spec/bespoke orders"
./bench/rmcli.py overlay add --id ov_2026-09-20_f14186 --address /v1/nodes/hard-diligence-legend-origin/body --why "need origin code for Austin (US)"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f14186 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k2/body
```

## Answer

Yes — a site visit is required. The file's re-review interval is every 6 months.

(Full row also states: screening score required 75, financial statements last three years audited — not asked for, but part of the same row.)

## Source

- /v1/nodes/hard-diligence-legend-origin/body — Austin → origin O3
- /v1/nodes/hard-diligence-legend-value/body — seven hundred million won → value W4
- /v1/nodes/hard-diligence-legend-goods/body — "something made to our spec" → goods K2
- /v1/nodes/hard-diligence-legend-revision/body — confirms today (2026-09-20) falls under the current table (in force from 2026-01-01), not the superseded v2 or original
- /v1/nodes/hard-diligence-row-origin-o3-value-w4-goods-k2/body — the answering row: site visit yes, re-review every 6 months

## Notes

- The three qualifiers mapped cleanly and exactly to legend entries — "Austin" → O3, "seven hundred million won" → W4, "something made to our spec" → K2 — all exact matches, no nearest-entry judgment calls needed.
- The one place this could have gone wrong is the version trap: `sec-hard-diligence` is the third rewrite of this subject, and the legend-revision page is explicit that reaching for the newest table is wrong for a question dated before 2026-01-01. Today's date (2026-09-20) is safely inside the current table's validity window, so no correction was needed here, but I checked the revision legend anyway before trusting the row rather than assuming the top-level table listing was current. Worth flagging that this same question asked about a 2025-dated event would require `hard-diligence-v2` instead, indexed by only two qualifiers, not three — a materially different lookup path.
- The overlay's initial member list also surfaced a parallel warning page for the *approval threshold* table (`hard-threshold-legend-revision`), which is a different subject (spend approval chain, not diligence) — not needed for this question, so I left it out of the working set rather than chase it.
