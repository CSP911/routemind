1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D1, hours H1, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01" --member /v1/nodes/hard-overtime-v2/body "superseded overtime version, kept to avoid confusing with current" --member /v1/nodes/hard-overtime-legend-revision/body "legend explaining which version covers which dates"
./bench/rmcli.py overlay remove --id ov_2026-09-20_252431 --address /v1/nodes/hard-overtime-v2/body --why "confirmed current table (2026-01-01) covers 2026-09-21, no need for superseded version"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_252431 --outcome answered --used /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p3/body

2. **Answer**: Multiplier 1.26x; minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p3/body

4. **Notes**: The attendance area lists overtime under three versions — a current table (`sec-hard-overtime`, in force from 2026-01-01), a superseded v2 (2024-07-01 to 2025-12-31), and an older one before that. Today's date (2026-09-21) falls under the current table, so I dropped the v2 member from the working set once that was confirmed rather than reading it. The overlay listed one row per (day, hours, place) combination directly under the table address rather than as separate documents I had to search for, so once the table opened, the exact row for D1/H1/P3 was already named — no ambiguity there. The only mild surprise was the overlay-close message noting the used address was "reached" rather than a named member, because I'd added the parent table as a member, not the individual row — this is just overlay bookkeeping and not a sign of a wrong answer.
