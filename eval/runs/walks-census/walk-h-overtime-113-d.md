1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p4/body

2. **Answer**: Multiplier is 1.89x. Minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p4/body

4. **Notes**: The path was straightforward — /v1/regions/attendance listed both a current overtime table (`sec-hard-overtime`, in force since 2026-01-01) and two superseded versions (`hard-overtime-v2`, `hard-overtime-legend-revision`). Since today's date is 2026-09-20, the current table was clearly the right one, but it would be easy to grab the superseded `hard-overtime-v2` row by mistake if not reading the descriptions carefully. The question already gave the row's codes (D2, H2, P4) literally, so no need to consult the day/hours/place legend files to translate a real-world scenario into codes — the row address was constructed directly from the table listing.
