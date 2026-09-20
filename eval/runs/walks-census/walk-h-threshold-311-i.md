1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m2/body

2. **Answer**
The department head signs it off, and two competing quotes are required. (Delegation limit for this row is 5,053 thousand KRW; working days to expect: 6.)

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body — confirms which of the three threshold table versions applies to today's date (2026-09-20/21 → current table)
- /v1/nodes/hard-threshold-legend-category/body — "dinner with a client" → category C4
- /v1/nodes/hard-threshold-legend-amount/body — "roughly 3 million won" → amount V2
- /v1/nodes/hard-threshold-legend-term/body — "renewing every year" → term M2
- /v1/nodes/hard-threshold-row-category-c4-amount-v2-term-m2/body — the row itself: signer and quote requirement

4. **Notes**
The approval threshold subject has three superseded/current versions covering different date ranges, and the legend-revision page warns that reaching for the newest version is wrong for any question dated before 2026-01-01, and that the oldest version says nothing about having been replaced (an easy trap if you just grabbed the first-looking match). Today's date (2026-09-20/21) is safely inside the current table's range (2026-01-01 onward), so no version confusion applied here, but I checked the revision page anyway rather than assuming the current table was correct by default.

The three qualifiers (category, amount, term) all happened to map cleanly onto exact legend entries — "dinner with a client," "roughly 3 million won," and "renewing every year" are near-verbatim matches to legend rows, so no nearest-entry judgment call was needed. That felt almost too easy given the legend's warning about inexact matches, which made me double-check each legend table rather than trust a skim.
