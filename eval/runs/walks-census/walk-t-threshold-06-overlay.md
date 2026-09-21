1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In August 2025, what was the delegation limit or who signed for category C2 spend in amount band V2? Under the version of approval threshold in force on that date." --member /v1/regions/procurement "approval threshold by category, amount and term - matches C2/V2 delegation question"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-v2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7250d9 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-v2/body

2. **Answer**:
5005 thousand KRW — the C2 / V2 delegation limit under the approval threshold version in force from 2024-07-01 to 2025-12-31 (which covers August 2025). The table gives this as an amount threshold, not a named signer role.

3. **Source**:
/v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three versions applies to a 2025 date)
/v1/nodes/hard-threshold-v2/body (the C2/V2 figure: 5005 thousand KRW)

4. **Notes**:
The approval threshold subject has three versions at different addresses (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the current one (`sec-hard-threshold`, in force from 2026-01-01) is the obvious but wrong pick for a 2025 date — the legend-revision page explicitly warns that reaching for the newest is wrong for anything before 2026-01-01, and that the oldest version says nothing about having been replaced, so nothing signals from the old doc alone that it's stale. Checked the legend first before reading any version, which avoided that trap. The table header in hard-threshold-v2 is "Who signs it, by category and amount" but its cells are all amounts, not role/title names — so "who signed" isn't independently answerable from this document; the delegation limit amount is the only figure available.
