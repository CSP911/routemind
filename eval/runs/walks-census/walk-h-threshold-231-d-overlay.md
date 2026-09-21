1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/procurement
./bench/rmcli.py overlay create --question "For category C3, amount V4, term M2, whose signature do I need, and do I have to get other prices first?" --member /v1/nodes/sec-hard-threshold "current approval threshold table, in force since 2026-01-01, likely has the category/amount/term matrix" --member /v1/nodes/hard-threshold-legend-revision/body "warns threshold has three versions with different dates - need to confirm which applies to today 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-threshold-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_21dc42 --outcome answered --used /v1/nodes/hard-threshold-legend-revision/body /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m2/body

2. **Answer**: Signed off by the division director. Yes — three competing quotes and a written comparison are required first. (Delegation limit for this row is 100,045 thousand KRW; expect 12 working days.)

3. **Source**:
- /v1/nodes/hard-threshold-legend-revision/body (confirmed today's date, 2026-09-21, falls under the current table)
- /v1/nodes/hard-threshold-row-category-c3-amount-v4-term-m2/body (the answer itself)

4. **Notes**: The procurement table lists three vintages of the approval-threshold subject (`threshold-table`, `hard-threshold-v2`, `sec-hard-threshold`), and the legend-revision page warns bluntly that grabbing the newest one is wrong for a question dated before 2026-01-01 — the oldest version doesn't even say it was superseded, so nothing there would flag the mistake. Today's date (2026-09-21) clearly falls in the "2026-01-01 onwards" band, so this case wasn't actually ambiguous, but it's the kind of question where skipping the date check would silently produce a stale answer with no error to catch it. Once inside the current table, the row for C3/V4/M2 existed exactly as named — no interpolation or fallback logic needed, unlike questions that fall between bands.
