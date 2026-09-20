## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p1/body

## Answer
Multiplier: 2.76x. Rounding: to the nearest 10 minutes.

## Source
/v1/regions/payroll (redirect notice: overtime rates moved to attendance on 2026-01-01)
/v1/regions/attendance (identified sec-hard-overtime as the current table, in force since 2026-01-01)
/v1/nodes/sec-hard-overtime (table of 64 rows, pointed to the three legends)
/v1/nodes/hard-overtime-legend-day/body (mapped "two in the morning" → day D4)
/v1/nodes/hard-overtime-legend-hours/body (mapped "three hours" → hours H2)
/v1/nodes/hard-overtime-legend-place/body (mapped "at my desk" → place P1)
/v1/nodes/hard-overtime-row-day-d4-hours-h2-place-p1/body (the answer: 2.76x, nearest 10 minutes)

## Notes
The main trap: "two in the morning" looks like a time-of-day qualifier that should feed the
*hours* axis, but the day-legend table claims it as a *day* code (D4) — the legend literally
lists "two in the morning" as a day-type example alongside "an ordinary Tuesday," "a Saturday,"
and "Liberation Day." Reading the row index (day/hours/place) before opening the legends could
easily lead to assuming D-codes are pure calendar days and searching for what calendar day
2026-09-20 fell on, or trying to fit "two in the morning" into the hours legend instead (where
it doesn't appear at all — hours there are pure durations: 90 min / 3h / 6h / 11h). Reading all
three legends before picking a row avoided that mistake. Also worth noting: payroll's old
overtime table is superseded and would have given a wrong (and differently-shaped) answer had I
stopped there instead of following the "moved to attendance on 2026-01-01" notice.
