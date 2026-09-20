## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p3/body

## Answer
Multiplier: 3.06x
Rounding: to the nearest 20 minutes
(Also noted on the row: approval needed in advance — yes; counts toward the monthly cap — yes.)

## Source
- /v1/nodes/hard-overtime-legend-day/body (maps "two in the morning" → day D4)
- /v1/nodes/hard-overtime-legend-hours/body (maps "eleven hours" → hours H4)
- /v1/nodes/hard-overtime-legend-place/body (maps "on standby at home" → place P3)
- /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p3/body (the figures)

## Notes
The three legend tables each contained the exact phrasing used in the question ("two in the
morning", "eleven hours", "on standby at home") as literal left-column entries, so no nearest-match
judgment call was needed — the mapping to D4/H4/P3 was exact, not approximate. The only place this
could have gone wrong: the attendance area table lists both a current overtime table
(`sec-hard-overtime`, in force since 2026-01-01) and a superseded one (`hard-overtime-v2`, 2024-07-01
to 2025-12-31), plus a `hard-overtime-legend-revision` node explaining the versioning. Today's date
(2026-09-20) falls under the current table, so `hard-overtime-v2` was correctly skipped, but a
careless walk could easily have opened the superseded version instead since both names look similar
at a glance.
