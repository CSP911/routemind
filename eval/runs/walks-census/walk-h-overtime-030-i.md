1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p1/body

2. **Answer**: Multiplier is 1.56x. Minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/regions/payroll (pointed to attendance as the current home for overtime rates)
/v1/nodes/hard-overtime-legend-revision/body (confirms current table applies from 2026-01-01, matching today's date 2026-09-20)
/v1/nodes/sec-hard-overtime (table index)
/v1/nodes/hard-overtime-legend-day/body ("an ordinary Tuesday" → day D1)
/v1/nodes/hard-overtime-legend-hours/body ("eleven hours" → hours H4)
/v1/nodes/hard-overtime-legend-place/body ("at my desk" → place P1)
/v1/nodes/hard-overtime-row-day-d1-hours-h4-place-p1/body (final answer: 1.56x, nearest 20 minutes)

4. **Notes**: The payroll region is the natural first instinct for anything with a "multiplier" (pay rate), and it does contain an overtime-looking node — but that region's own table header and the `hard-moved-overtime` file flag that overtime premiums moved to attendance on 2026-01-01, so payroll would have been a wrong turn if followed further. The attendance region then has a legend-revision file warning that overtime rate has three versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward) with the explicit caution that reaching for the newest is wrong for anything before 2026-01-01 — today's date (2026-09-20) falls in the current window, so `sec-hard-overtime` was correct, but this was the one place a careless walk could have grabbed the wrong version. The three qualifiers (day/hours/place) each needed their own legend lookup since none of the plain-English terms in the question ("ordinary Tuesday," "eleven hours," "at my desk") appear directly in the row table — they only make sense after translating through the legends to D1/H4/P1.
