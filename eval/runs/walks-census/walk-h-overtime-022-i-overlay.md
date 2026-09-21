1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "An ordinary tuesday, six hours, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table since 2026-01-01, likely has multiplier by day type/hours/place, standby at home may be a 'place'"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_a54a3b --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p3/body

2. **Answer**: Multiplier 1.50x; rounding to the nearest 15 minutes. (Current table, in force from 2026-01-01.)

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h3-place-p3/body

4. **Notes**: The three qualifiers ("ordinary Tuesday", "six hours", "on standby at home") each had to be translated through a separate legend file before the row address could be built — the rows themselves give no hint of the underlying meaning (D1/H3/P3 are opaque without the legends). The three legends map cleanly and exactly to the question's wording ("an ordinary Tuesday" → D1, "six hours" → H3, "on standby at home" → P3), so no nearest-match judgment call was needed here. The only place I could have gone wrong is picking the superseded overtime table (hard-overtime-v2, or the even older overtime-rate-table) instead of the current sec-hard-overtime one — the attendance table listing flags both, and since the question gives no date, I used today's date context (2026-09-20/21) to confirm the current (2026-01-01-onward) table applies.
