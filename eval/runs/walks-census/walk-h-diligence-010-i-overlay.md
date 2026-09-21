1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "Daejeon company, KRW 60,000,000 contract, office consumables only: site visit required? review/renewal frequency?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table, in force since 2026-01-01, likely has site visit + review frequency by origin/value/goods" --member /v1/nodes/sec-supplier-due-diligence "overview of how the four due-diligence pages fit together, may clarify which page has review cadence" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions; need to confirm which is current for today's date"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a3bc64 --outcome answered --used /v1/nodes/hard-diligence-legend-origin/body /v1/nodes/hard-diligence-legend-value/body /v1/nodes/hard-diligence-legend-goods/body /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k1/body

2. **Answer**: No, no site visit is required. The file is re-reviewed every 24 months. (This is the row for origin O1 = Daejeon, value W2 = sixty million won, goods K1 = office consumables only, in the current supplier due diligence table, in force 2026-01-01 onward — which covers today, 2026-09-21.)

3. **Source**:
/v1/nodes/hard-diligence-legend-origin/body
/v1/nodes/hard-diligence-legend-value/body
/v1/nodes/hard-diligence-legend-goods/body
/v1/nodes/hard-diligence-legend-revision/body
/v1/nodes/hard-diligence-row-origin-o1-value-w2-goods-k1/body

4. **Notes**: The row addresses (e.g. `hard-diligence-row-origin-o1-value-w2-goods-k1`) look guessable from the legends, but I read the actual row rather than constructing the address from pattern-matching alone — the overlay table had already printed it verbatim, so no address was invented. The real risk here was the version trap: the procurement table lists three supplier due diligence tables (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`) and explicitly warns that reaching for the newest is wrong for anything before 2026-01-01. Since today is 2026-09-21, the current (three-qualifier) table is correct, but I deliberately read the revision-legend page to confirm the date window rather than assuming "current" meant "newest" — the warning text says exactly that assumption is the trap for 2025-dated questions, and I wanted to be sure I wasn't in that band. Also worth flagging: the question gives Daejeon/60M won/office-consumables in plain English, and the legends explicitly say the mapping is written down nowhere else — every qualifier had to be resolved through its own legend page rather than inferred.
