1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p3/body

2. **Answer**: Multiplier 2.58x, rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p3/body (also consulted /v1/nodes/hard-overtime-legend-revision/body to confirm which of the three overtime-rate versions applies to today's date)

4. **Notes**: This subject has three superseded versions of the overtime rate table (`overtime-rate-table`, `hard-overtime-v2`, `sec-hard-overtime`), and the legend-revision page explicitly warns that reaching for the newest one is wrong for dates before 2026-01-01, and that the oldest table says nothing about having been replaced. Since the question gives no date, I used today's date (2026-09-20), which falls under the current table (`sec-hard-overtime`, in force from 2026-01-01) — the one indexed by all three qualifiers (day, hours, place), matching the D3/H4/P3 shape of the question. Had the question specified an earlier date, the middle version (`hard-overtime-v2`) would likely have applied instead. The current table's index conveniently has one row per exact (day, hours, place) combination, so no interpolation or legend lookup was needed once the right table version was identified.
