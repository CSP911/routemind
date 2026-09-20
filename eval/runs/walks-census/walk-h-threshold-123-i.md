1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-category/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-amount/body
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-term/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m4/body

2. **Answer**
"A consultant's time" is category C2, "around 12 million won" is amount V3, "until we cancel it" is term M4.
For C2 / V3 / M4: the division director signs it off, and three competing quotes are required (delegation limit 20,027 thousand KRW; 11 working days to expect).

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (confirms which version applies as of 2026-09-20/21)
/v1/nodes/hard-threshold-legend-category/body
/v1/nodes/hard-threshold-legend-amount/body
/v1/nodes/hard-threshold-legend-term/body
/v1/nodes/hard-threshold-row-category-c2-amount-v3-term-m4/body

4. **Notes**
The three-legend indexing (category/amount/term) is easy to get wrong if you jump straight to a row address without checking all three legends first — "a consultant's time," "around 12 million won," and "until we cancel it" map almost verbatim onto legend rows, but nothing forces you to check the term legend if you're not alert to "until we cancel it" being a term qualifier rather than just color on the amount. The revision-legend warning was the other near-miss: there are three versions of this threshold table (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward), and grabbing the newest without checking today's date (2026-09-20/21) against the legend would have been right here by luck, not by process — for a question dated in 2025 it would have been wrong. Nothing else in the walk was ambiguous.
