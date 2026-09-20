1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p1/body

2. **Answer**: Multiplier is 1.92x; minutes are rounded to the nearest 15 minutes. (This row also requires advance approval and counts toward the monthly cap.)

3. **Source**:
/v1/nodes/sec-hard-overtime (table listing, confirms this is the current table, in force since 2026-01-01)
/v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p1/body (the row itself, containing the multiplier and rounding figures)

4. **Notes**: The attendance table listed both a current overtime table (`sec-hard-overtime`, in force from 2026-01-01) and a superseded one (`hard-overtime-v2`, 2024-07-01 to 2025-12-31), plus a "legend-revision" doc warning of three historical versions. Since today is 2026-09-20, the current table is the right one, but it would have been easy to grab the superseded `hard-overtime-v2` body by mistake since its title also mentions "day, hours, place" style content — the naming is very similar and only the "SUPERSEDED" vs "THE CURRENT ... TABLE" wording in the description disambiguates it. Also didn't need the day/hours/place legends since D2/H3/P1 were given directly as codes in the question, matching the row address format exactly.
