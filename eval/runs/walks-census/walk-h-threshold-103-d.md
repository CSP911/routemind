1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m4/body

2. **Answer**
Signature: the department head signs it off.
Other prices: no — competing quotes required is "none."
(Context: delegation limit 1,019 thousand KRW; working days to expect: 5. In force from 2026-01-01.)

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold table versions applies to today's date)
/v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m4/body (the answer)

4. **Notes**
The procurement area holds three superseded versions of the approval threshold subject (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns explicitly that reaching for the newest is wrong for dates before 2026-01-01. Today's date (2026-09-20/21) falls in the current version's range, so `sec-hard-threshold` was correct, but this was the one place a careless walk could have grabbed the wrong row without checking dates — worth flagging since the older two versions were not even excluded from the table listing, they just sat there alongside the current one under the same procurement table. The question already gave the codes (C2, V1, M4) directly, so no separate lookup in the amount/category/term legend files was needed to translate a plain-language description into codes.
