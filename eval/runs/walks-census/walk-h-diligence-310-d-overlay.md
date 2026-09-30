1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O4, value W2, goods K1: is a premises visit required, and what is the re-review (file look-at-again) frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, likely has the by-origin/value/goods matrix with site visit and review frequency columns" --member /v1/nodes/hard-diligence-legend-revision "warns of three versions of diligence rules; need to confirm which is in force for 2026-09-21" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together, may clarify terms like premises visit and re-review"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k1/body
./bench/rmcli.py overlay remove --id ov_2026-09-20_4c9140 --address /v1/nodes/sec-supplier-due-diligence --why "not needed once the exact three-qualifier row was found directly"
./bench/rmcli.py overlay close --id ov_2026-09-20_4c9140 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k1/body

2. **Answer**:
No premises (site) visit is required. The file is re-reviewed every 24 months.
(For reference, this row also requires a screening score of 82 and last year's financial statements — not asked, but part of the same row.)

3. **Source**:
- /v1/nodes/hard-diligence-legend-revision/body — confirmed which of the three due-diligence table versions is in force for 2026-09-21 (the current one, `sec-hard-diligence`, effective 2026-01-01 onward, indexed by three qualifiers: origin/value/goods)
- /v1/nodes/hard-diligence-row-origin-o4-value-w2-goods-k1/body — the row itself, giving "Site visit: no" and "Re-review interval: every 24 months"

4. **Notes**:
The procurement area table lists both a superseded diligence page (`hard-diligence-v2`, in force 2024-07-01 to 2025-12-31) and the current one (`sec-hard-diligence`), plus a legend-revision page warning that there are actually three versions total and that guessing "newest" is wrong for dates before 2026-01-01. It would have been easy to grab `hard-diligence-v2` by pattern-matching on "the one with origin/value/goods" without checking the date — the legend-revision page exists specifically to catch that, and confirmed today's date (2026-09-20/21) falls under the current table, indexed by three qualifiers, matching the row found. Also worth flagging: the row document's closing section, "If the figures are exceeded," reads like boilerplate about travel/expense overage claims (budget holder, unrecoverable excess) rather than anything about supplier diligence — it's out of place for this document and I did not use it, but another reader could mistake it for part of the diligence answer.
