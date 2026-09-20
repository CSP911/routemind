1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p4/body

2. **Answer**
Multiplier: 2.97x. Rounding: to the nearest 15 minutes. (Also: approval needed in advance — yes; counts toward the monthly cap — yes.)

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p4/body

4. **Notes**
The trap here is in the payroll area: the payroll table lists an overtime page (`hard-moved-overtime`) that warns overtime premiums moved to attendance on 2026-01-01, so the payroll page itself is stale — had to follow the pointer to attendance rather than trust the first hit.

Bigger trap is the day legend. "Two in the morning" reads like a time-of-day qualifier that would modify an hours band, but the legend table actually maps it directly to a *day* code, D4 — sitting in the same list as "an ordinary Tuesday," "a Saturday," and "Liberation Day." It would be easy to either discard "two in the morning" as irrelevant once "six hours" was mapped to hours, or to mistakenly try to fold it into the hours/place axes. It's its own axis value and has to be looked up in the day legend specifically.

Also confirmed there are two "home" place values — "on standby at home" (P3) and "from home" (P4) — which are easy to conflate. The question said "from home," which is P4, not P3; picking the wrong one changes the row entirely.

All three legends explicitly cover the exact values in the question (D4, H3, P4), so no nearest-entry approximation was needed — the row was an exact match, not an inferred one.
