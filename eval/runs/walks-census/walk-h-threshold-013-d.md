1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m4/body

2. **Answer**
For category C1, amount V2, term M4 (current table, in force 2026-01-01 onward — applies to today, 2026-09-20): the division director signs it off. Yes, other prices are required first — two competing quotes. Delegation limit is 5007 thousand KRW, and 8 working days should be expected.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold-table versions is current for today's date)
/v1/nodes/hard-threshold-row-category-c1-amount-v2-term-m4/body (the actual figures)

4. **Notes**
The procurement area lists three overlapping "approval threshold" pages (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`) with no obvious marker on the oldest one that it's been superseded — the legend-revision page exists specifically to warn about this and says the naive move (grabbing the newest table, or the alphabetically-first one) is wrong for dates before 2026-01-01. Today's date (2026-09-20) falls under the current table `sec-hard-threshold`, so this walk was straightforward once the legend was checked, but skipping that check would have been an easy mistake — the old `threshold-table` "says nothing at all about having been replaced," per the legend page itself. Since the question already gave codes in the table's own indexing scheme (C1/V2/M4), the category/amount/term legend pages weren't needed to translate plain-language qualifiers into codes.
