1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Ordinary Tuesday, 3 hours overtime, from home: what multiplier applies, and to what rounding are minutes taken?" --member /v1/regions/attendance "overtime hours/rules likely under attendance" --member /v1/regions/payroll "overtime pay multiplier likely under payroll"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_bff636 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p4/body

2. **Answer**: Multiplier 1.41x. Rounding: to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p4/body

4. **Notes**: The overtime table has three superseded versions with different indexing (one, two, then three qualifiers), and the revision-legend page warns that taking "the newest" is wrong for a pre-2026 date. Today (2026-09-20/21) falls after the 2026-01-01 cutover, so `sec-hard-overtime` (the three-qualifier table) was the right one to use — easy to get right here, but this is clearly the trap the walk is testing for on other dates. The three plain-language qualifiers ("an ordinary Tuesday", "three hours", "from home") each had to be translated through a separate legend page into row codes (D1, H2, P4) before the actual row address could be constructed — none of the codes are guessable, and each legend explicitly says it's the only place that mapping exists. No ambiguity in the mapping itself: all three inputs matched a legend row exactly (no need to fall back to "nearest entry above").