1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body

2. **Answer**: Under the approval threshold version in force 2024-07-01 to 2025-12-31 (the version covering March 2025), category C2 at amount band V2 has a delegation limit of **5005 thousand KRW**. The table does not name an individual signer for this cell — it only gives the amount threshold; who signs at that level was unchanged from the prior ("approval thresholds") rule and not restated in this version.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body
/v1/nodes/hard-threshold-v2/body

4. **Notes**: The procurement area lists three separate documents for "approval threshold" (oldest `threshold-table`, middle `hard-threshold-v2`, current `sec-hard-threshold`), and the region/table listing surfaces only the current one (`sec-hard-threshold`, "in force from 2026-01-01") plus the middle one as "SUPERSEDED" — it would be easy to grab the current table by reflex since it's the one flagged "THE CURRENT ... TABLE" and never open the legend page. The legend page (`hard-threshold-legend-revision`) explicitly warns that for a 2025-dated question the middle version applies, not the oldest and not the current one — that's what redirected me to `hard-threshold-v2`. Also worth flagging: the v2 table's header says "Who signs it, by category and amount" but the cells are all KRW amounts, not names/roles — so this version answers "delegation limit" but not "who signed" as a name; that part of the question may be genuinely unanswered by this document.
