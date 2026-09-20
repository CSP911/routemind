1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-supplier-due-diligence
./bench/rmcli.py read /v1/nodes/sec-supplier-due-diligence/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k2/body

2. **Answer**
No, a site visit is not required. The file is re-reviewed every 24 months.
(Origin: "a vendor in Austin" = O3; "sixty million won" = W2; "something made to our spec" = K2 — row O3/W2/K2, in force since 2026-01-01.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (confirmed current version applies to today's date)
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-row-origin-o3-value-w2-goods-k2/body

4. **Notes**
The due-diligence subject has three versions (legend-revision page warns of this explicitly) — the oldest page never says it was superseded, so checking the revision legend before trusting any table was necessary. Today (2026-09-20) falls after 2026-01-01, so the current table `sec-hard-diligence` was correct to use; a 2025-dated question would need `hard-diligence-v2` instead, not the current or oldest table.

The `sec-supplier-due-diligence` overview page mentioned "a fourth page covering the ongoing side of the same checks, re-run rather than one-off" but never named it explicitly among its four listed children — I nearly went down that path looking for a separate "ongoing review" document, but the actual re-review cadence turned out to live directly in the row-level table (`sec-hard-diligence`) as a "Re-review interval" field, not in a separate standalone page. That overview section was a red herring for this specific question.

Mapping all three qualifiers (origin/value/goods) required three separate legend lookups before the row address could be constructed — none of the codes are guessable from the question wording alone, and the legends explicitly warn not to build an address without checking them.
