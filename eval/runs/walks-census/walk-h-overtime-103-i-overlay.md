1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Saturday, about ninety minutes, from home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/weekend work time rules likely live here" --member /v1/regions/payroll "overtime multiplier and pay calculation likely documented here"
./bench/rmcli.py overlay remove --id ov_2026-09-20_4b16bf --address /v1/nodes/annual-leave --why "not overtime related"
./bench/rmcli.py table ov_2026-09-20_4b16bf
./bench/rmcli.py overlay remove --id ov_2026-09-20_4b16bf --address /v1/nodes/annual-leave --why "not overtime related"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_4b16bf --outcome answered --used /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p4/body

2. **Answer**: Multiplier 1.77x. Rounding: to the nearest 5 minutes. (Current table, in force from 2026-01-01; today is 2026-09-20/21, so this version applies.)

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
/v1/nodes/hard-overtime-legend-hours/body (about ninety minutes → hours H1)
/v1/nodes/hard-overtime-legend-place/body (from home → place P4)
/v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p4/body (the rate row itself: multiplier and rounding)

4. **Notes**: The legends map each qualifier to a code exactly, no approximation needed — "a Saturday" is D2 verbatim, "about ninety minutes" is H1 verbatim, and "from home" is P4 verbatim. The one place I nearly slipped was the place legend: it has two home-adjacent entries, "on standby at home" (P3) and "from home" (P4), which look interchangeable at a glance but are different codes with presumably different rates — worth reading the whole legend rather than stopping at the first "home" match. I also tried to prune the overlay's attendance sub-rows with `overlay remove`, which failed (404, "not in this overlay") — the overlay's actual members are just the two region tables I passed with `--member`; the long row lists printed under them are previews of that region's contents, not overlay members, so `remove` only applies to explicitly-added members. That cost one wasted call but didn't block the walk. The row document also names two superseded versions (`hard-overtime-v2` for 2024-07-01–2025-12-31, and `overtime-rate-table` before that) — I did not need to open either since today's date falls inside the current table's in-force window, but a walker working a past date would need to check `hard-overtime-legend-revision` instead.
