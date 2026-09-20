1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m3/body

2. **Answer**
Dinner with a client (category C4), about 40 million won (amount V4), locked in for three years (term M3) → the division director signs it off. Three competing quotes and a written comparison are required first. Delegation limit for this row is 100,062 thousand KRW; expect 13 working days.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirms today's date, 2026-09-20, falls under the current table)
/v1/nodes/hard-threshold-legend-category/body ("dinner with a client" → category C4)
/v1/nodes/hard-threshold-legend-amount/body ("about 40 million won" → amount V4)
/v1/nodes/hard-threshold-legend-term/body ("locked in for three years" → term M3)
/v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m3/body (the answer row: signer, quotes)

4. **Notes**
The three qualifiers (category, amount, term) map almost word-for-word onto the phrasing in the question ("dinner with a client", "about 40 million won", "locked in for three years"), which made it easy to feel confident about the row picked — but that's exactly the trap: there are three versions of this threshold table (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and grabbing the newest one without checking the legend-revision page first would have been an assumption, not a check. The revision page explicitly warns the oldest version "says nothing at all about having been replaced," so it doesn't announce its own supersession — you have to know to look. Today's date (2026-09-20) is safely after 2026-01-01, so `sec-hard-threshold` is correct, but I only trust that because I read the revision doc before picking a row, not after. No other ambiguity: the legend tables are literal 1:1 phrase matches, so no interpretation was needed once the right table version was confirmed.
