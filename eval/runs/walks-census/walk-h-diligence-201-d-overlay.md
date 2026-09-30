1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For origin O3, value W1, goods K2, do we have to go and see their premises, and how often does their file get looked at again?" --member /v1/nodes/sec-hard-diligence "current supplier due diligence table by origin/value/goods, in force since 2026-01-01" --member /v1/nodes/hard-diligence-legend-revision/body "warns of three versions of due diligence rules, need to confirm which applies to today's date 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_e3aec9 --outcome answered --used /v1/nodes/hard-diligence-legend-revision/body /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k2/body

2. **Answer**
No — a site visit is not required for origin O3, value W1, goods K2.
The file is re-reviewed every 36 months (screening score required: 63; financial statements: not required).
This is from the current due-diligence table, in force since 2026-01-01, which applies to today's date (2026-09-21).

3. **Source**
- /v1/nodes/hard-diligence-legend-revision/body (confirmed which of the three due-diligence table versions applies to today's date)
- /v1/nodes/hard-diligence-row-origin-o3-value-w1-goods-k2/body (the row with the site-visit and re-review figures)

4. **Notes**
The near-miss here was version drift, not row-finding: the procurement table lists three eras of the
supplier due-diligence subject (`supplier-due-diligence`, `hard-diligence-v2`, `sec-hard-diligence`),
and the legend-revision page is explicit that reaching for the newest is wrong for anything dated
before 2026-01-01, and that the oldest version never says it was superseded. Since the question carries
no explicit date, I anchored on today's date (2026-09-21), which falls after 2026-01-01, so the current
table (`sec-hard-diligence`) is the right one — but this is exactly the kind of question where grabbing
the first plausible-looking row without checking the revision legend would silently give the wrong
answer for a question meant to be read against an earlier date.

One mechanical wrinkle: adding `/v1/nodes/sec-hard-diligence` as an overlay member expanded it into all
64 of its underlying origin/value/goods rows (one per O×W×K combination) rather than staying as a single
row — so the exact row I needed (O3/W1/K2) was already sitting in the working set after creation, and I
read it directly rather than using `overlay add`. The close command flagged this row as "reached" rather
than a named member for that reason; it's a bookkeeping note, not a sign the answer is shaky — the row is
squarely inside the table I deliberately picked.
