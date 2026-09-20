1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p2/body

2. **Answer**: Multiplier 2.67x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
- /v1/regions/payroll (found the redirect notice)
- /v1/nodes/hard-moved-overtime/body (confirms overtime moved to attendance, effective 2026-01-01)
- /v1/regions/attendance
- /v1/nodes/sec-hard-overtime (current overtime rate table, in force since 2026-01-01)
- /v1/nodes/hard-overtime-legend-day/body (maps "two in the morning" → day D4)
- /v1/nodes/hard-overtime-legend-hours/body (maps "about ninety minutes" → hours H1)
- /v1/nodes/hard-overtime-legend-place/body (maps "out at a client's office" → place P2)
- /v1/nodes/hard-overtime-row-day-d4-hours-h1-place-p2/body (the answer row)

4. **Notes**: The natural first stop is payroll, since overtime pay sounds like a payslip question — but payroll only holds the pre-2026 rule now, with an explicit warning redirecting to attendance's `sec-hard-overtime` for anything on or after 2026-01-01. Today is 2026-09-20, so the payroll page (`payslip-overtime`) would have been the wrong source had I not read the redirect notice first.

The trickiest part was the "day" legend. I expected D1–D4 to encode weekday/Saturday/holiday-type categories, and assumed I'd need to guess or ask what day of the week the 2am shift fell on. Instead the legend's own rows show it isn't a calendar-day classification at all — "an ordinary Tuesday," "a Saturday," "Liberation Day," and "two in the morning" are all treated as parallel entries in the same lookup, so a literal time-of-night phrase maps directly to D4 without needing any date. This is worth flagging: the table's column is called "day" but one of its four values is actually a time-of-day condition, which isn't obvious from the row list alone.

The hours and place legends were straightforward exact matches ("about ninety minutes" → H1, "out at a client's office" → P2), so no interpolation via the "nearest entry above it" fallback was needed anywhere.
