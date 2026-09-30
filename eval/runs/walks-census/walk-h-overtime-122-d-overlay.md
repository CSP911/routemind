1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D2, hours H3, place P3, what multiplier applies, and to what rounding are minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01" --member /v1/nodes/hard-overtime-legend-revision/body "warns overtime rate has three versions with different date ranges - need to confirm which applies"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_efafaa --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p3/body

2. **Answer**: Multiplier is 1.98x; minutes are rounded to the nearest 15 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed the current, three-qualifier table applies since the question is undated and today, 2026-09-21, falls in the 2026-01-01-onwards range)
- /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p3/body (the multiplier and rounding figures)

4. **Notes**: This walk was straightforward because the overtime table is indexed by exactly the three qualifiers the question gives (day, hours, place), and the overlay's table listing surfaced the exact row address (`hard-overtime-row-day-d2-hours-h3-place-p3`) without needing to guess or construct it. The one place to be careful was the revision warning: overtime rate has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onwards), and the warning explicitly flags that reaching for the newest is wrong for anything before 2026-01-01. The question itself carries no date, so I anchored on today's date (2026-09-21) rather than assuming the current table — it happens to land in the current range, but this is exactly the kind of question where a dated version elsewhere (2025-06 in the sample question) would require the superseded `hard-overtime-v2` table instead. Did not need to add/remove overlay members since the exact row was already listed under the `sec-hard-overtime` member from creation.
