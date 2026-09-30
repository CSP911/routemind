1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Two in the morning, about ninety minutes, at my desk: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime multiplier and minute rounding are likely attendance policy topics" --member /v1/regions/payroll "overtime pay multiplier could be documented as a payroll rule"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-21_bfc07e --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p1/body

2. **Answer**: Multiplier 2.64x. Minutes are rounded to the nearest 5 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed the current, 2026-01-01-onward table is the right version for a 2026-09-20 question)
- /v1/nodes/sec-hard-overtime (index of the current overtime rate table)
- /v1/nodes/hard-overtime-legend-day/body (two in the morning → day D4)
- /v1/nodes/hard-overtime-legend-hours/body (about ninety minutes → hours H1)
- /v1/nodes/hard-overtime-legend-place/body (at my desk → place P1)
- /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p1/body (the answer: 2.64x, nearest 5 minutes)

4. **Notes**: The question's three clauses map suspiciously literally onto the three legends' example rows ("two in the morning" is literally the D4 example, "about ninety minutes" is literally the H1 example, "at my desk" is literally the P1 example) — easy to feel like you're being handed the answer rather than deriving it, but that's just how the legends are written, and each mapping still had to be checked against its own table rather than assumed. The real trap was the revision warning: the domain has three overtime-rate versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward), and jumping straight to "the current one" without reading `hard-overtime-legend-revision` first would have worked here only by luck, since 2026-09-20 does fall in the current window — but the revision note explicitly warns that for a 2025-dated question the middle version applies instead, so skipping that check is a real way to get this kind of question wrong on a different date. Also worth flagging: this row's overtime counts toward the monthly cap as "no" and requires advance approval — not asked here, but a natural follow-up.
