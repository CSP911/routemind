1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C4, amount V1, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table, in force since 2026-01-01, likely has category/amount/term matrix with signer and quote requirement"
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_d8bb07 --outcome answered --used /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m3/body

2. **Answer**: The department head signs it off. No competing quotes are required (Competing quotes: none). Delegation limit for this row is 1,050 thousand KRW, with 4 working days to expect.

3. **Source**: /v1/nodes/hard-threshold-row-category-c4-amount-v1-term-m3/body

4. **Notes**: The overlay create against /v1/nodes/sec-hard-threshold auto-expanded into the full current threshold table (all C1–C4 × V1–V4 × M1–M4 rows), which made it trivial to spot the exact row by its address (category-c4-amount-v1-term-m3) without needing the legend files to translate raw figures/durations into C/V/M codes — the question was already phrased in the table's own notation. I did not open the legend or revision-warning files, since the row itself states it's "in force from 2026-01-01" and today is 2026-09-21/20, so it's current; the row also names the two prior superseded versions (hard-threshold-v2, threshold-table) for context, which confirmed I wasn't looking at a stale copy. One mildly confusing thing: `overlay close --used` reported the address as "reached ... from somewhere the overlay never named" even though it was one of the rows the overlay table itself printed — apparently only addresses added via explicit `overlay add`/`create --member` count as "named" members, not rows surfaced incidentally in a printed table. Didn't affect the answer, just a quirk of the bookkeeping.
