1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m2/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**:
For category C2, amount V2, term M2 (current approval threshold table, in force 2026-01-01 onwards): the **department head** signs it off. Yes, other prices are required first — **two competing quotes**. (Delegation limit for this row is 5,021 thousand KRW; expect 6 working days.)

3. **Source**:
- /v1/nodes/hard-threshold-row-category-c2-amount-v2-term-m2/body (main answer: signer, quotes required)
- /v1/nodes/hard-threshold-legend-revision/body (confirms this row's table, `sec-hard-threshold`, is the correct version for today's date, 2026-09-21)

4. **Notes**:
The question gave the codes C2/V2/M2 directly, so I never needed to open the amount/category/term legend files to translate real-world values into codes — that saved a step but is also a trap: this table has three superseded versions (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), each indexed differently (one, two, then three qualifiers), and the region table's row list surfaces the two older ones right alongside the current one with only a warning in their descriptions. It would be easy to grab `hard-threshold-v2`'s row by mistake since it sits higher/near in the listing and shares similar naming. I explicitly checked `hard-threshold-legend-revision` to confirm 2026-09-21 falls under the current (2026-01-01 onwards) table before trusting the row I'd already read — worth doing even when the exact row address seems obviously right, since the codes C2/V2/M2 exist identically in more than one version of this table.
