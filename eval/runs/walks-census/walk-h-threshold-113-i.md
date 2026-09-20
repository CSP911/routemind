1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m4/body

2. **Answer**
A consultant's time, roughly 3 million won, running until cancelled maps to category C2, amount V2, term M4 in the current approval threshold table (in force 2026-01-01 onward, which covers today, 2026-09-21). For that row: the division director signs it off, and two competing quotes are required before approval. The delegation limit for this row is 5,023 thousand KRW, and working days to expect is 8.

3. **Source**
- /v1/regions/procurement (found the approval threshold area)
- /v1/nodes/sec-hard-threshold (confirmed current table, three-qualifier index)
- /v1/nodes/hard-threshold-legend-category/body (consultant's time → C2)
- /v1/nodes/hard-threshold-legend-amount/body (roughly 3 million won → V2)
- /v1/nodes/hard-threshold-legend-term/body (until we cancel it → M4)
- /v1/nodes/hard-threshold-legend-revision/body (confirmed date 2026-09-21 falls under the current table, not the superseded ones)
- /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m4/body (final answer row)

4. **Notes**
The threshold table has three superseded/current versions and the legend-revision page warns explicitly that reaching for the newest version is wrong for dates before 2026-01-01 — easy to get wrong if you skip that check. Today's date (2026-09-21) is safely inside the current table's range, so no ambiguity there, but it was worth verifying rather than assuming the top-listed table was current. The three qualifiers (category, amount, term) each have their own legend page with an explicit "if not listed, take the nearest entry" instruction, and the wording in the question ("a consultant's time," "roughly 3 million won," "until we cancel it") matched the legend rows' phrasing closely enough that no nearest-entry judgment call was needed — all three mapped exactly. The one place I could have gone wrong: mistaking "until we cancel it" for "renewing every year" (M2) since both describe ongoing engagements, but the legend text draws a clear line — M2 is a periodic renewal, M4 is open-ended with no fixed renewal cycle — and "until we cancel it" is verbatim the M4 row.
