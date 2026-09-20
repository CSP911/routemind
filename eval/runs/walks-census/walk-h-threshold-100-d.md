1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m1/body

2. **Answer**
For category C2, amount V1, term M1: the team lead signs it off. No competing quotes are required ("Competing quotes: none") — you do not have to get other prices first. (Delegation limit for this row is 1,016 thousand KRW; expect 2 working days.)

3. **Source**
/v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m1/body

4. **Notes**
The procurement region table listed both a current table (`/v1/nodes/sec-hard-threshold`, in force from 2026-01-01) and two superseded threshold tables (`hard-threshold-v2` and, further back, `threshold-table`), plus a `hard-threshold-legend-revision` page warning there are three versions. It would have been easy to grab an old row by mistake. I didn't need to open the legend-revision file separately because the `sec-hard-threshold` table's own header already stated it is "THE CURRENT APPROVAL THRESHOLD TABLE, in force from 2026-01-01" with no end date, and today's date (2026-09-21) falls inside that range, so this is unambiguously the right version. The row address itself (`hard-threshold-row-category-c2-amount-v1-term-m1`) matched the question's C2/V1/M1 exactly, so no legend lookups for category/amount/term codes were needed either — the table printed the row directly.
