1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body

2. **Answer**
5005 thousand KRW — the amount threshold for category C2, amount band V2, under the approval threshold version in force from 2024-07-01 to 2025-12-31 (which covers October 2024). No specific signer name/role is given for this cell; the table only lists the KRW figure per category/amount-band combination.

3. **Source**
/v1/nodes/hard-threshold-legend-revision/body (to identify which of the three threshold versions applies to October 2024)
/v1/nodes/hard-threshold-v2/body (the version in force 2024-07-01 to 2025-12-31, containing the C2/V2 figure)

4. **Notes**
The procurement table lists three separate threshold documents (an oldest one at `threshold-table`, `hard-threshold-v2`, and the current `sec-hard-threshold`), each superseding the last but none marked withdrawn. It would have been easy to grab `sec-hard-threshold` since it's labeled "THE CURRENT APPROVAL THRESHOLD TABLE" and listed last/prominently — but that one only took effect 2026-01-01, well after the October 2024 date in the question. The legend-revision page explicitly warns that reaching for the newest table is wrong for any date before 2026-01-01, and that the oldest table (pre-2024-07-01) says nothing about being replaced, so date-checking against the legend was necessary rather than assuming. October 2024 falls squarely in the 2024-07-01–2025-12-31 window, so `hard-threshold-v2` is correct. That table's header is "Who signs it, by category and amount" but the cell values are KRW thresholds, not names/roles — no distinct signer identity is given for C2/V2 in this version, so I reported the amount and did not fabricate a signer.
