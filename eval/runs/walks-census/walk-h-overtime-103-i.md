1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p4/body

2. **Answer**: Multiplier 1.77x; minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/sec-hard-overtime (table, to find the legends and rows)
/v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
/v1/nodes/hard-overtime-legend-hours/body ("about ninety minutes" → hours H1, exact wording match)
/v1/nodes/hard-overtime-legend-place/body ("from home" → place P4, exact wording match)
/v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p4/body (the answer: 1.77x, nearest 5 minutes)

4. **Notes**: The three legends (day, hours, place) each map a plain description to a code letter, and the row address is built from those three codes concatenated — easy to mis-key if you don't read all three legends first. "About ninety minutes" and "from home" are both exact phrases in their respective legend tables, so no interpolation or nearest-match judgment was needed here, which removed one source of ambiguity the legends explicitly warn about ("if what you have is not listed, take the nearest entry"). The attendance area's table listing also surfaces a superseded row (`hard-overtime-row-...` doesn't exist, but `hard-overtime-v2` and `overtime-rate-table` do as older versions) — I confirmed I was on the current table (`sec-hard-overtime`, in force since 2026-01-01, which matches today's date 2026-09-20) rather than one of the two superseded overtime tables mentioned in the legend-revision warning. Did not need to open that revision-warning file since the "current" label and the effective date were unambiguous.
