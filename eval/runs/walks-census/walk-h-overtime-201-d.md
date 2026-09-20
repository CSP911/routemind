1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p2/body

2. **Answer**: Multiplier is 2.19x. Minutes are rounded to the nearest 5 minutes.

3. **Source**:
- /v1/nodes/hard-overtime-legend-revision/body (confirmed which of the three overtime versions applies to today's date, 2026-09-20)
- /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p2/body (the row with the answer)

4. **Notes**: The `/v1/regions/payroll` table led straight to a trap: it lists overtime pay as one of its "why you would be here" reasons, but the table header itself warns overtime premiums moved to attendance on 2026-01-01, and there's a `hard-moved-overtime` stub node confirming payroll is stale for this subject. Easy to grab the wrong region here if you don't read the header text.

Inside attendance, there's a second trap: three separate overtime documents exist (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and the legend-revision doc explicitly warns that reaching for the newest is wrong for dates before 2026-01-01, and that the oldest doc doesn't self-identify as superseded. Since today is 2026-09-20, the current table (`sec-hard-overtime`, in force 2026-01-01 onward, indexed by day/hours/place — matching this question's three qualifiers D3/H1/P2) was the correct one, but I only knew that for certain because I checked the revision-legend doc first rather than assuming "current" was safe by default. Once at the row level, the address matched the D3/H1/P2 pattern exactly, so no ambiguity there.
