1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m3/body

2. **Answer**
"A consultant's time" = category C2. "About 700,000 won" = amount V1. "Locked in for three years" = term M3. For C2/V1/M3: the department head signs it off, and no competing quotes are required (delegation limit for this row is 1018 thousand KRW, so 700,000 won is within it).

3. **Source**
- /v1/nodes/hard-threshold-legend-category/body (mapped "a consultant's time" to C2)
- /v1/nodes/hard-threshold-legend-amount/body (mapped "about 700,000 won" to V1)
- /v1/nodes/hard-threshold-legend-term/body (mapped "locked in for three years" to M3)
- /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m3/body (the answer: department head signs, no competing quotes needed)

4. **Notes**
The procurement region table listed several superseded threshold pages (hard-threshold-v2, threshold-table) alongside the current one — sec-hard-threshold is explicitly marked as in force from 2026-01-01, which covers today (2026-09-21), so I used it and did not need to check the older versions. The three legends (category, amount, term) had to be read separately and combined by hand into the row address (c2-amount-v1-term-m3) — the row list itself gives no hint which combination matches plain-language wording, so skipping any one legend would have made it impossible to build the correct address. Nothing else stood out as ambiguous; the wording in the legends mapped cleanly onto the question's phrasing ("a consultant's time", "about 700,000 won", "locked in for three years").
