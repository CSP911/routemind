1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m1/body
```

2. **Answer**
For category C1, amount V1, term M1 (current table, in force from 2026-01-01): the team lead signs it off, and no competing quotes are required (delegation limit 1,000 thousand KRW; 2 working days to expect).

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (established which version applies for today's date, 2026-09-20)
- /v1/nodes/sec-hard-threshold (current threshold table, confirmed the row exists as a literal code, not a placeholder)
- /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m1/body (the answer)

4. **Notes**
The question's "C1, V1, M1" looked at first glance like unfilled template placeholders rather than real values — worth pausing on, since answering blindly against the wrong assumption (e.g. treating them as generic examples, or picking the wrong table version) would have been easy. Two things resolved it: (1) the procurement table explicitly warned that approval-threshold has three versions covering different date ranges and that reaching for the newest without checking the date is wrong — today (2026-09-20) falls in the 2026-01-01-onwards current version, so that risk was real and worth checking rather than assuming; (2) once inside the current table, C1/V1/M1 turned out to be the table's actual row-code vocabulary (categories c1–c4, amounts v1–v4, terms m1–m4), and a row literally named for exactly this combination existed at a predictable address, so no legend lookup for category/amount/term definitions was needed — the row was addressed directly by the codes given in the question.
