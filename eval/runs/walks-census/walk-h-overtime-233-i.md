1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p4/body

2. **Answer**
Multiplier: 2.61x. Rounding: to the nearest 20 minutes.

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p4/body

4. **Notes**
Two places to go wrong here. First, the attendance area's table listed both `sec-hard-overtime` (current, in force from 2026-01-01) and `hard-overtime-v2` (superseded, 2024-07-01 to 2025-12-31) plus a still-older `overtime-rate-table`. Today is 2026-09-20, so the current table is the right one — but it would be easy to grab the first overtime row that looked plausible without checking which version window applies.

Second, the day legend is genuinely odd: it maps "Liberation Day" to D3 by name/date, but also maps "two in the morning" to D4, which is a time-of-day, not a day-of-week or holiday. That mixing means you cannot assume the axis is purely about calendar day type — you have to read each legend entry literally rather than pattern-matching. "Liberation Day" matched a legend row exactly (D3), so no fuzzy "nearest entry" judgment was needed there. "Eleven hours" and "from home" also both matched their legend rows exactly (H4, P4), so the whole lookup was exact-match, no interpolation required — which is worth flagging since the legends explicitly allow for nearest-entry substitution when there's no exact match, and I want it clear I didn't need to invoke that fallback.
