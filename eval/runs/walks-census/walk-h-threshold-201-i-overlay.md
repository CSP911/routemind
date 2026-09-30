1. Commands

./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Flights and hotels, about 700,000 won, renewing every year: whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "amount + term-based approval threshold for a category — procurement table covers this directly"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_418945 --outcome answered --used /v1/regions/procurement /v1/nodes/sec-hard-threshold /v1/nodes/hard-threshold-legend-category /v1/nodes/hard-threshold-legend-amount /v1/nodes/hard-threshold-legend-term /v1/nodes/hard-threshold-legend-revision /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m2

2. Answer

Signature: the team lead. Competing quotes: none required. (Delegation limit for this row is 1,033 thousand KRW; working days to expect: 3.)

Flights and hotels map to category C3, about 700,000 won maps to amount V1, and renewing every year maps to term M2, giving row C3/V1/M2 in the current approval threshold table (in force 2026-01-01 onwards, which covers today's date).

3. Source

/v1/regions/procurement
/v1/nodes/sec-hard-threshold
/v1/nodes/hard-threshold-legend-category
/v1/nodes/hard-threshold-legend-amount
/v1/nodes/hard-threshold-legend-term
/v1/nodes/hard-threshold-legend-revision
/v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m2

4. Notes

The approval threshold subject has three versions (threshold-table, hard-threshold-v2, sec-hard-threshold) and a legend-revision page warns that "the oldest says nothing at all about having been replaced" — reaching for the newest version without checking is the trap. Today's date (2026-09-20) falls in the 2026-01-01-onwards window, so the current table (sec-hard-threshold) was correct, but this had to be verified explicitly rather than assumed. The three legends (category, amount, term) are each the *only* place their mapping is written, and none of it is repeated in the row table itself, so all three had to be fetched before the row address could even be constructed. Nothing else was ambiguous — the mappings were unambiguous (700,000 won → V1, flights and hotels → C3, renewing every year → M2), and the row directly answered both parts of the question (signer and quote requirement).
