1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m1/body

2. **Answer**
The department head signs it off. Yes — three competing quotes and a written comparison are required first.
(Delegation limit for this row: 100,028 thousand KRW; expect 11 working days.)

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" → category C2)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "about 40 million won" → amount V4)
- /v1/nodes/hard-threshold-legend-term/body (mapped "just the once" → term M1)
- /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m1/body (the answer: signer and quote requirement)

4. **Notes**
The procurement table lists three superseded/parallel threshold pages (`hard-threshold-legend-revision`, `hard-threshold-v2`, and the current `sec-hard-threshold`) alongside a warning that there are three versions with different date ranges. It would have been easy to grab `hard-threshold-v2` by mistake since it sorts near the current table in the listing — its own label makes clear it was superseded 2025-12-31, so with today's date (2026-09-21) the current table (`sec-hard-threshold`, in force since 2026-01-01) is the right one. The row address itself must be hand-built from three legend lookups (category, amount, term) rather than being handed to you directly — each legend explicitly says "this is the only place the mapping is written down," so skipping any one of them risks guessing the wrong row address. All three qualifiers ("a consultant's time," "about 40 million won," "just the once") matched an exact legend entry, so no nearest-value judgment call was needed here.
