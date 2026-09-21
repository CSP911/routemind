1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C1, amount V1, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term is procurement's stated purpose"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_ec93dc --outcome answered --used /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m4/body

2. **Answer**: For category C1, amount V1, term M4: the department head signs it off. No competing quotes are required (Competing quotes: none). Delegation limit for this row is 1003 thousand KRW, with 5 working days to expect.

3. **Source**: /v1/nodes/hard-threshold-row-category-c1-amount-v1-term-m4/body (reached via table /v1/nodes/sec-hard-threshold).

4. **Notes**: The procurement table warned that the approval threshold table has THREE versions (a `hard-threshold-legend-revision` node) — `threshold-table` (oldest), `hard-threshold-v2` (2024-07-01 to 2025-12-31), and the current `sec-hard-threshold` (in force from 2026-01-01). It would have been easy to grab the superseded `hard-threshold-v2` row by mistake since it sorts near the current one in the working set and looks structurally identical. Today's date (2026-09-21) falls inside the current table's validity window, and the row body itself restates "In force from 2026-01-01," which was enough to confirm without a separate legend lookup. Also worth flagging: when I closed the overlay, the tool reported the used address as "reached" rather than matching a named member — I had only added the parent `/v1/regions/procurement` table as a member, not the specific row address, so the close command treated it as reached-but-unlisted. Doesn't affect the answer, just a quirk of how the working set was built.
