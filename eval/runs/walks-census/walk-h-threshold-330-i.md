1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/corp-card
./bench/rmcli.py read /v1/nodes/corp-card/body
./bench/rmcli.py read /v1/nodes/expense-overview/body
./bench/rmcli.py table /v1/nodes/card-limit
./bench/rmcli.py table /v1/nodes/entertainment
./bench/rmcli.py read /v1/nodes/entertainment/body
./bench/rmcli.py read /v1/nodes/entertainment-limit/body
./bench/rmcli.py table /v1/nodes/sec-entertainment-cases
./bench/rmcli.py read /v1/nodes/entertainment-fixed-headcount-event/body
./bench/rmcli.py table /v1/nodes/sec-spending-that-needs-a-draft-first
./bench/rmcli.py read /v1/nodes/expense-draft-approval-overview/body
./bench/rmcli.py read /v1/nodes/expense-draft-approval-threshold-table/body
./bench/rmcli.py table /v1/regions/approval
./bench/rmcli.py read /v1/nodes/hard-moved-threshold/body
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/sec-hard-threshold/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m1/body

2. **Answer**
The department head signs it off. Yes — three competing quotes plus a written comparison are required before booking. (Delegation limit for this row is 100,060 thousand KRW, so 40 million won is within the department head's authority; expect 11 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m1/body

4. **Notes**
The obvious first path is Expense > Corporate card > Entertainment — "dinner with a client" reads like a per-head meal cap question (50,000 KRW/head), and I went fairly deep into that section (entertainment-limit, entertainment-fixed-headcount-event, the draft-approval threshold table) before realizing none of those pages name a signer for an amount this large or say anything about competing quotes. That whole branch turned out to be a near-miss: it's the right area for policing a normal client meal, but 40 million won for one dinner is a scale the entertainment cap doesn't address at all, and chasing "overage approval" language there would have led to a guess rather than an answer.
The real key was the approval region's warning (hard-moved-threshold) that spend thresholds moved to procurement as of 2026-01-01 — the approval region's own threshold rules are stale for today's date (2026-09-20) and would have given a wrong answer if used.
The category legend was the sharpest turn: "dinner with a client" is listed there verbatim as the example for category C4, which is a strong signal this is the intended path rather than the entertainment-cap one. Likewise "about 40 million won" and "just the once" are the exact example phrasings for V4 and M1, so no rounding/nearest-band judgment call was needed — a rare case where the legend examples matched the question word-for-word instead of requiring interpolation.
