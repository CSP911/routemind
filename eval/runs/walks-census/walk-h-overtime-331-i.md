1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p2/body

2. **Answer**: Multiplier 3.03x; minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/regions/payroll
/v1/regions/attendance
/v1/nodes/sec-hard-overtime
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p2/body

4. **Notes**: The first instinct is to look under payroll, since overtime rates sound like a pay question — but the payroll region itself warns that overtime/night/holiday premiums moved to attendance on 2026-01-01, and the payroll copy is explicitly the old, superseded rule. Following that pointer to attendance avoided citing a dead rate.

The three legends line up suspiciously well with the question's exact wording ("two in the morning" → D4, "eleven hours" → H4, "out at a client's office" → P2), each an exact match rather than a "nearest entry above it" judgment call — so there was no ambiguity in which row to pick, but it's worth flagging that all three phrases were lifted verbatim from the legends, which made this walk easier than a real-world version of the same question would likely be (real inputs rarely land exactly on a legend entry).

Also worth noting: attendance itself carries three historical versions of the overtime table (`hard-overtime-v2`, `overtime-rate-table`, and the current `sec-hard-overtime`), with a legend-revision file warning about which dates each covers. Since today is 2026-09-20 and the current table took effect 2026-01-01, `sec-hard-overtime` is correct, but a careless walk could have grabbed one of the two superseded tables by name alone.
