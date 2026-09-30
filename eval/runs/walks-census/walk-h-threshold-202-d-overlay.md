1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C3, amount V1, term M3, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term lives in this table"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_91951f --outcome answered --used /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m3/body /v1/nodes/hard-threshold-legend-revision/body

2. **Answer**:
Signature: the department head signs off. No competing quotes are required (competing quotes: none). Delegation limit for this row is 1034 thousand KRW, with 4 working days to expect. (This is the current table, in force from 2026-01-01.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed which of the three threshold-table versions applies to a 2026-dated question — the current one)
- /v1/nodes/hard-threshold-row-category-c3-amount-v1-term-m3/body (the row itself: signer, quotes, limit, turnaround)

4. **Notes**:
The procurement region table doesn't show the threshold table directly — it surfaces two "hard-threshold" nodes (a legend-revision warning and a superseded v2 body) plus the current `sec-hard-threshold` table, and it's easy to grab the wrong one. The legend-revision page is explicit that the domain has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward) and that the oldest version doesn't announce that it was ever replaced, so date-checking is mandatory rather than optional. Since the question carries no date, I used today (2026-09-20/21 per the two conflicting reminders in this session — both fall after 2026-01-01), which puts it squarely in the current table, so this wasn't actually a close call here, but it would have been if the question were dated in 2025.
Once inside `sec-hard-threshold`, the table lists all 64 category×amount×term row files, and C3/V1/M3 has an exact, unambiguous address — no need to open the category/amount/term legend files since the codes were given directly in the question.
I tried to prune the overlay's suggested rows (vendor, ga-desk, due-diligence, etc.) that came pre-listed under the /v1/regions/procurement member, but the CLI returned 404 for all of them — they were display-only suggestions from the parent table, never actual overlay members, so removal wasn't applicable. Worth knowing for future walks: only addresses added explicitly via `--member`/`add` are real members; the rest of a table's listing is just visible context, not something you need to (or can) remove.
