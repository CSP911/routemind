1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Daejeon supplier, 700M KRW, custom-spec (made to our spec): mandatory site visit and periodic re-review frequency?" --member /v1/regions/procurement "custom-spec supplier vetting, site visits, and periodic review cadence would be procurement policy"
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_b2cbce --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k2/body

2. **Answer**: Yes, a site visit is required. The file gets re-reviewed every 6 months.

3. **Source**:
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-row-origin-o1-value-w4-goods-k2/body

4. **Notes**: The `/v1/regions/procurement` table surfaced two due-diligence entry points — `sec-supplier-due-diligence` (the four-page narrative overview: disqualification triggers, sanctions checks, code of conduct, general due-diligence doc) and `sec-hard-diligence` (the 64-row lookup table keyed by origin/value/goods codes). The narrative overview looked like the natural first stop but doesn't contain per-band figures like site-visit requirement or re-review interval — those only live in the coded row table. Also had to actively check the "legend-revision" warning: `sec-hard-diligence` is explicitly the version in force from 2026-01-01, and today (2026-09-20/21) falls inside that window, so no need to consult the superseded `hard-diligence-v2` or original `supplier-due-diligence` version — but it would have been easy to grab the wrong vintage without reading that note. Translating the question's plain-language terms to codes was the crux: "Daejeon" → O1, "seven hundred million won" → W4 (the top band, not W3's three hundred million), and "something made to our spec" → K2, matching the legend's own example phrase almost verbatim. The overlay's `close --used` call reported all four addresses as "reached" rather than "used" because they were never formally added as overlay members (only the top-level procurement region was) — worth noting since I only browsed to them via table/read rather than tracking them in the overlay itself.
