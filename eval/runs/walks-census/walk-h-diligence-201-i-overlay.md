1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Vendor in Austin, 8M KRW, made-to-spec: site visit required? how often re-reviewed?" --member /v1/regions/procurement "procurement covers approval thresholds and vendor rules by amount/category/term"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9db644 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/sec-hard-diligence /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k2/body

2. **Answer**
No, a site visit is not required. The file is re-reviewed every 36 months.
(Screening score required: 63; financial statements not required — for context, not asked.)

3. **Source**
/v1/nodes/hard-diligence-legend-revision/body (established which of the three versions applies to today's date, 2026-09-20)
/v1/nodes/sec-hard-diligence (current table index, in force from 2026-01-01)
/v1/nodes/hard-diligence-legend-origin/body (Austin → origin O3)
/v1/nodes/hard-diligence-legend-value/body (eight million won → value W1)
/v1/nodes/hard-diligence-legend-goods/body (something made to our spec → goods K2)
/v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k2/body (the answering row: site visit no, re-review every 36 months)

4. **Notes**
The legend-revision page was the thing to check first and not skip — this subject has three versions (old `supplier-due-diligence`, `hard-diligence-v2` for 2024-07-01–2025-12-31, and the current `sec-hard-diligence` for 2026-01-01 onward), and the old version "says nothing at all about having been replaced," so jumping straight to `sec-hard-diligence` without checking the date would have worked here only by luck. Today's date (2026-09-20) falls cleanly in the current window, so no ambiguity in this case, but it's the kind of check that's easy to skip and wrong to skip.

Also worth flagging: overlay close reported these addresses as "reached" rather than "used" — I never added them as explicit overlay members, only the parent `/v1/regions/procurement` region, so the tool doesn't recognize the deeper addresses as named working-set members even though they're exactly what answered the question. Didn't affect the answer, but the overlay mechanics only track what you explicitly add as a member, not everything you read along the path.

The three qualifiers (origin/value/goods) each have their own legend page and none of it is repeated in the row itself — all three had to be resolved before the row address could even be constructed, and each legend explicitly says "take the nearest entry above it" if there's no exact match. Here all three matched exactly (Austin, eight million won, something made to our spec), so no judgment call was needed, but that fallback rule is easy to miss on a first read.
