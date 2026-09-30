1. Commands

./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/corp-card
./bench/rmcli.py overlay create --question "Dinner with a client, about 40 million won, just the once: whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/corp-card "corporate card caps section, may cover entertainment cap" --member /v1/nodes/sec-spending-that-needs-a-draft-first "over-cap spend likely needs a draft/approval before it happens" --member /v1/regions/approval "need to find whose signature is required for this amount"
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_6c71f1 --outcome answered --used /v1/nodes/hard-moved-threshold/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m1/body

2. Answer

The department head signs it off. Yes — three competing quotes plus a written comparison are required first. (This spend, ~40M won, is within the row's delegation limit of 100,060 thousand KRW, so nothing is being exceeded.)

3. Source

/v1/nodes/hard-threshold-legend-category/body (maps "dinner with a client" → category C4)
/v1/nodes/hard-threshold-legend-amount/body (maps "about 40 million won" → amount V4)
/v1/nodes/hard-threshold-legend-term/body (maps "just the once" → term M1)
/v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m1/body (the row itself: department head signs, three quotes + written comparison, delegation limit 100,060 thousand KRW)
/v1/nodes/hard-moved-threshold/body (redirect: from 2026-01-01 spend approval thresholds live in procurement's sec-hard-threshold, not in approval)

4. Notes

My first instinct was to start in /v1/regions/expense (dinner with a client reads as an entertainment expense) and then /v1/regions/approval (for "whose signature"), and I built the initial overlay around those. Both were dead ends for this specific question: expense's corp-card/draft-approval pages never actually named a per-category threshold table, and approval turned out to be superseded for this — /v1/nodes/hard-moved-threshold/body says spend approval thresholds moved to procurement's sec-hard-threshold as of 2026-01-01, and today (2026-09-21) is after that cutover. If I hadn't opened that warning file I'd have kept digging in approval and could easily have surfaced the pre-2026 rule (`delegation-scope`) instead, which is now wrong.

The threshold table itself is a 64-row grid keyed by three independently-coded legends (category C1-C4, amount V1-V4, term M1-M4) rather than by plain language, and each legend explicitly says "if what you have is not listed, take the nearest entry above it" — a trap for the amount band in particular. Here all three mapped exactly to the example wording in the question ("dinner with a client" = C4, "about 40 million won" = V4, "just the once" = M1), so no nearest-neighbor judgment call was needed, but it would be easy to get this wrong on a question with less on-the-nose amount.
