1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m2/body

2. **Answer**: The department head signs it off, and yes — three competing quotes are required first. This row's delegation limit is 20,025 thousand KRW (~20 million won), so the ~12 million won amount falls within the department head's authority.

3. **Source** (in order used):
/v1/regions/procurement
/v1/nodes/sec-hard-threshold
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m2/body

4. **Notes**: The three legends (category, amount, term) each had to be resolved separately before the row address could be assembled — "a consultant's time" maps to category C2, "around 12 million won" maps to amount V3, and "renewing every year" maps to term M2, giving the row `hard-threshold-row-category-c2-amount-v3-term-m2`. It would have been easy to grab an outdated row: the procurement table lists two superseded threshold versions (`hard-threshold-v2` and an even older one referenced via `hard-threshold-legend-revision`) alongside the current one, and the row list under `sec-hard-threshold` doesn't repeat the "current" caveat per row — only the table header and the row body's own footnote confirm this is the 2026-01-01-onward version, which is the one that applies for today's date (2026-09-21). Nothing here was ambiguous once the three legends were checked; the only risk was jumping straight to a guessed row address instead of deriving it from the legends.
