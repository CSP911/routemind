## Commands

```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/supplier-due-diligence/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k4/body
```

## Answer

Yes, a site visit is required. The file is re-reviewed every 6 months.

(Stuttgart → origin O2, seven hundred million won → value W4, a licence → goods K4; row O2/W4/K4 in the current supplier due diligence table.)

## Source

- /v1/nodes/hard-diligence-legend-origin/body (mapped "Stuttgart" to O2)
- /v1/nodes/hard-diligence-legend-value/body (mapped "seven hundred million won" to W4)
- /v1/nodes/hard-diligence-legend-goods/body (mapped "a licence" to K4)
- /v1/nodes/hard-diligence-row-origin-o2-value-w4-goods-k4/body (answer: Site visit yes, re-review every 6 months)

## Notes

- The `procurement` region table warns up front that supplier due diligence has three versions with overlapping-looking date ranges (a legend-revision page exists specifically to disambiguate). I didn't need to open `hard-diligence-legend-revision` because the row's own footer states plainly it's "in force from 2026-01-01" with no end date, and today is 2026-09-20 — so it's current on its face. Worth flagging that I trusted the row's self-reported validity window rather than cross-checking the legend-revision page; if that page ever contradicts individual rows' footers, this answer would need revisiting.
- I nearly stopped at `supplier-due-diligence/body` (the pre-2026 general description), which discusses sanctions/code-of-conduct/disqualification checks but says nothing about site visits or re-review cadence — that's a dead end for this specific question. The actual numbers only live in the indexed origin/value/goods matrix (`sec-hard-diligence`), not in the narrative pages.
- The matrix is keyed by codes (O2/W4/K4), not by the words in the question, and each axis has its own legend file that must be read separately before the row address can be constructed. Getting any one axis wrong (e.g. picking the wrong value band) silently points at a different row with different answers, with no cross-check offered by the tool.
