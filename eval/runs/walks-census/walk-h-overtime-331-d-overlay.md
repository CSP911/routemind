1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D4, hours H4, place P2, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place - directly matches D4/H4/P2 axes" --member /v1/nodes/hard-overtime-legend-revision/body "warns which version is in force for what dates - need to confirm current table applies"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-21_fe1441 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p2/body

2. **Answer**: Multiplier is 3.03x; minutes are rounded to the nearest 20 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed the current table, in force from 2026-01-01, applies since no other date was given and today is 2026-09-21)
- /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p2/body (the figures)

4. **Notes**: The overlay's table listing for /v1/nodes/sec-hard-overtime printed a full grid of row addresses for every day/hours/place combination, including the exact one needed (hard-overtime-row-day-d4-hours-h4-place-p2), so the row address didn't need to be constructed — it was right there. The one thing worth checking carefully was the revision warning: overtime rate has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), and the legend explicitly warns that reaching for the newest is wrong for dates before 2026-01-01 and that the oldest page never says it was superseded. Since the question gave no date, I used today's date (2026-09-21) to confirm the current table (sec-hard-overtime, in force 2026-01-01 onward) is the right one — this matched the row I'd already found. The overlay close reported the row as "reached" rather than a named member, since I'd only added the parent table address as a member, not the individual row leaf — worth noting but not an issue, since the leaf was visible directly under that table.
