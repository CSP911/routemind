1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m1/body

2. **Answer**
Sign-off: the team lead. Competing quotes: none required. (Delegation limit for this row is 1,016 thousand KRW; ~700,000 won and a one-off engagement both fall within it — 2 working days to expect.)

3. **Source**
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c2-amount-v1-term-m1/body

4. **Notes**
The procurement region table flags up front that the approval-threshold subject has three superseded versions (`threshold-table`, `hard-threshold-v2`, and the current `sec-hard-threshold`), with a legend-revision page explaining which dates each covers. It would have been easy to grab `hard-threshold-v2` by mistake since it sorts before the current table alphabetically and its description also reads as plausible ("in force from 2024-07-01..."). I went with `sec-hard-threshold` because it's explicitly labeled the current table and today (2026-09-21) falls after its 2026-01-01 start date — worth double-checking on any question like this since picking a superseded row would give a wrong signer/quote answer with no error signal.

The three-way lookup (category/amount/term legends -> row address) is also a place to go wrong: "a consultant's time" isn't a verbatim category name, it's listed as its own row in the category legend, and "about 700,000 won" maps exactly to V1 with no rounding ambiguity, so no "nearest entry" judgment call was needed here. The row address itself must be hand-assembled from the three codes (c2-v1-m1) since the table listing doesn't spell out the mapping — got it right on the first try but it's the one spot a typo would silently 404 or point at a neighboring row.
