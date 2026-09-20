1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m2/body

2. **Answer**
Sign-off: the department head. Competing quotes required: two. (Delegation limit for this row is 5,021 thousand KRW, comfortably above the ~3 million won described; expected turnaround is 6 working days.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" → category C2)
/v1/nodes/hard-threshold-legend-amount/body (mapped "roughly 3 million won" → amount V2)
/v1/nodes/hard-threshold-legend-term/body (mapped "renewing every year" → term M2)
/v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m2/body (the answer: sign-off and quote count)

4. **Notes**
The procurement table lists both the current approval-threshold table (`sec-hard-threshold`, in force since 2026-01-01) and a superseded one (`hard-threshold-v2`, 2024-07-01 to 2025-12-31) side by side, plus a legend-revision warning page. It would be easy to grab the wrong version by pattern-matching on the filename alone — I only trusted `sec-hard-threshold` because its own listing explicitly states it's current and dated 2026-01-01, which is before today's date (2026-09-21) with no newer version superseding it.

The three qualifiers (category, amount, term) are each resolved by a separate legend table, and none of them repeat the plain-English input verbatim — you have to translate "a consultant's time" / "roughly 3 million won" / "renewing every year" into codes first, then find the one row matching all three. It would be easy to guess a row address instead of reading it off the table listing; I confirmed the exact row address (`hard-threshold-row-category-c2-amount-v2-term-m2`) was printed verbatim in the `sec-hard-threshold` table before reading it, rather than constructing it myself.
