1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m2/body

2. Answer
Signature: the division director.
Other prices required first: yes — three competing quotes plus a written comparison.
(Delegation limit for this row: 100,013 thousand KRW; expect 12 working days.)

3. Source
/v1/nodes/hard-threshold-legend-revision/body (established 2026-09-20 falls under the current, 2026-01-01-onwards version, not the two older ones)
/v1/nodes/hard-threshold-legend-category/body (a couple of laptops → category C1)
/v1/nodes/hard-threshold-legend-amount/body (about 40 million won → amount V4)
/v1/nodes/hard-threshold-legend-term/body (renewing every year → term M2)
/v1/nodes/hard-threshold-row-category-c1-amount-v4-term-m2/body (the answer)

4. Notes
The approval threshold subject has three superseded versions of the same table (threshold-table, hard-threshold-v2, sec-hard-threshold), and the table listing at /v1/regions/procurement surfaces the old hard-threshold-v2 file right alongside the current one with no visual distinction until you actually open the legend-revision page — easy to grab the wrong one if you don't check dates first. Today (2026-09-20) is safely inside the current table's range (2026-01-01 onwards), so no ambiguity here, but the revision page's own warning implies a 2025-dated question would have needed the middle version instead of either extreme — worth remembering for other walks.

The three qualifiers (category, amount, term) each have their own legend file, and none of them let you guess the code without reading the mapping table explicitly — e.g. "a couple of laptops" isn't obviously C1 without checking, and "renewing every year" easily could be misread as M4 ("until we cancel it") if skimmed too fast rather than M2. All three legends had to be read in full before touching the row.
