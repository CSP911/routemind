1. Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m2/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body

2. Answer
A consultant's time (category C2), about 40 million won (amount band V4), renewing every year (term M2) needs sign-off from the division director. Three competing quotes plus a written comparison are required. (Delegation limit for this row is 100,029 thousand KRW; expect 12 working days.)

3. Source
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c2-amount-v4-term-m2/body
/v1/nodes/hard-threshold-legend-revision/body (used to confirm the current table applies to today's date)

4. Notes
The approval threshold subject has three superseded versions (threshold-table, hard-threshold-v2, sec-hard-threshold), and the region table and the procurement table both list old and current pages side by side without flagging which is which — the legend-revision page is the only thing that states plainly that anything from 2026-01-01 onward uses the current three-qualifier table, so I checked it before trusting the row I'd found. It was easy to jump straight to a row address by guessing the codes, but the instructions are explicit that addresses must never be constructed — I fetched each of the three legends (category, amount, term) separately to turn "consultant's time / 40 million won / renewing every year" into C2/V4/M2, and only then used the resulting address exactly as it appeared in the sec-hard-threshold table listing. The category legend's "a consultant's time" wording matches the question closely enough that there was no ambiguity there; the amount legend's "about 40 million won" is also an exact phrase match to the question, so no band-rounding judgment call was needed.
