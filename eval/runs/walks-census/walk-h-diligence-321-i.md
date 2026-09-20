1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-diligence
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-origin/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-value/body
./bench/rmcli.py read /v1/nodes/hard-diligence-legend-goods/body
./bench/rmcli.py read /v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k2/body

2. **Answer**
Yes, a site visit is required. The file (screening) is re-reviewed every 12 months.
(Screening score required: 87; financial statements: last two years — for context.)

3. **Source**
/v1/nodes/hard-diligence-legend-origin/body (Da Nang → origin O4)
/v1/nodes/hard-diligence-legend-value/body (300 million won → value W3)
/v1/nodes/hard-diligence-legend-goods/body (something made to our spec → goods K2)
/v1/nodes/hard-diligence-row-origin-o4-value-w3-goods-k2/body (final answer)

4. **Notes**
There are three versions of the supplier due diligence table with overlapping validity, and the
legend-revision page warns explicitly that "reaching for the newest is wrong for anything before
2026-01-01." Today's date (2026-09-20) falls after the 2026-01-01 cutover, so the current table
(`sec-hard-diligence`) was correct — but this is the kind of question where checking the date
first is essential; a 2025-dated question would need `hard-diligence-v2` instead, and neither
older version marks itself as superseded, so guessing from the newest table without checking
dates would silently give a wrong answer for older questions.

All three qualifiers (Da Nang, 300 million won, "something made to our spec") matched a legend
row exactly, with no need to fall back to "nearest entry above" — so no rounding/approximation
judgment call was needed here, which simplified things.
