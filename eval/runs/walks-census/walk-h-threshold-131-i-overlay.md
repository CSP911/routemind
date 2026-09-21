1. Commands

./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Consultant's time, about 40 million won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "threshold/approval and competitive-quote requirement lives in procurement region"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_9eeedc --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-legend-category/body /v1/nodes/hard-threshold-legend-amount/body /v1/nodes/hard-threshold-legend-term/body /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m2/body

2. Answer

The division director signs it off. Yes — three competing quotes and a written comparison are required. (Delegation limit for this row is 100,029 thousand KRW; expect 12 working days.)

3. Source

/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m2/body

4. Notes

The approval threshold subject has three superseded/current versions covering different date ranges, with an explicit warning that reaching for the newest is wrong for any date before 2026-01-01. Today is 2026-09-21, so the current table (`sec-hard-threshold`, in force from 2026-01-01) was correct here, but this is exactly the trap the legend page calls out — a question dated in 2025 would need `hard-threshold-v2` instead, and the oldest table says nothing about being superseded, so skipping the revision-legend check could silently give a stale answer. The row itself is indexed by three separate qualifiers (category, amount, term), each resolved through its own legend table rather than any obvious inference: "a consultant's time" only maps to C2 via the category legend, and "renewing every year" only maps to M2 via the term legend — neither is guessable from the row address alone. No ambiguity in the final row lookup once the three codes were resolved.
