1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m2/body

2. **Answer**
For category C4, amount V4, term M2 (current table, in force from 2026-01-01): signature required is the division director. Yes, other prices are required first — three competing quotes plus a written comparison. Delegation limit is 100,061 thousand KRW; expect 12 working days.

3. **Source**
/v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m2/body

4. **Notes**
The procurement area lists three versions of the approval-threshold subject (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and a warning page (`hard-threshold-legend-revision`) explicitly says reaching for the newest is wrong for dates before 2026-01-01. Today is 2026-09-20/21, so the current table (`sec-hard-threshold`) is correct, but this was the one place a wrong turn was easy: without checking the revision-legend page first, it would have been tempting to just open `sec-hard-threshold` directly since it's labeled "current" and skip verifying the date actually falls in its range. The question's own phrasing (C4, V4, M2) matches the current table's three-qualifier indexing exactly, which was a useful confirmation that this is the right version rather than an older one indexed by fewer qualifiers. Did not need the amount/category/term legend pages since the codes were given directly in the question and matched an address verbatim.
