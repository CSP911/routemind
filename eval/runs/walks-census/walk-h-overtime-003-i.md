1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p4/body

2. **Answer**: Multiplier is 1.29x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-day/body (ordinary Tuesday → day D1)
- /v1/nodes/hard-overtime-legend-hours/body (about ninety minutes → hours H1)
- /v1/nodes/hard-overtime-legend-place/body (from home → place P4)
- /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p4/body (the answer: 1.29x, nearest 5 minutes)

4. **Notes**: The three legends (day, hours, place) had to be read separately before the row address could be assembled — the table listing alone doesn't map plain-language phrasing to the D/H/P codes, and guessing at a row address instead of reading the legends would have been easy to get wrong. One near-miss: the day legend's D4 entry is "two in the morning," a time rather than a day type, which could tempt a misread if skimmed quickly — but "an ordinary Tuesday" matches D1 exactly, so no ambiguity there. Also confirmed via `sec-hard-overtime`'s own description that this is the current table (in force from 2026-01-01, superseding `hard-overtime-v2` and `overtime-rate-table`), so no version-selection issue for today's date (2026-09-20).
