1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "October 2024 delegation limit / signer for category C2 spend, amount band V2, under threshold version in force then" --member /v1/regions/procurement "approval threshold by category, amount and term - likely holds C2/V2 delegation limits"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_9b8cf7 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-v2/body

2. **Answer**
Under the version of the approval threshold in force on 2024-10 (the 2024-07-01 to 2025-12-31 version, `hard-threshold-v2`), category C2 spend in amount band V2 has a delegation limit of **5,005 thousand KRW**. The table gives this as an amount, not a named signer — who actually signs at that level is stated only as following "the approval thresholds rule unchanged until 2026-01-01," which this page does not itself restate.

3. **Source**
- /v1/nodes/hard-threshold-legend-revision/body (used to confirm which of the three threshold versions covers October 2024)
- /v1/nodes/hard-threshold-v2/body (the version in force 2024-07-01–2025-12-31; contains the C2/V2 figure)

4. **Notes**
The overlay's opening table listed three threshold-related documents at once: `hard-threshold-legend-revision`, `hard-threshold-v2`, and `sec-hard-threshold` (the current table, in force only from 2026-01-01). It would have been easy to grab `sec-hard-threshold` by reflex since it's labeled "THE CURRENT APPROVAL THRESHOLD TABLE" — that table does not apply to a 2024 date and uses three qualifiers (category, amount, term) instead of two, so C2/V2 there would mean something different or be indexed differently. The legend-revision page was the one that resolved this, explicitly warning that reaching for the newest table is wrong for anything before 2026-01-01, and confirming October 2024 falls under the middle (`hard-threshold-v2`) version. Also worth flagging: the v2 table's header says "Who signs it, by category and amount" but the cells are all KRW amounts, not names or roles — so a literal "who signed" answer isn't available from this page; only the delegation-limit amount is.
