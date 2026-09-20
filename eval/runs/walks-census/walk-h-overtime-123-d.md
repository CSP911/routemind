1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p4/body

2. **Answer**
Multiplier: 2.01x. Minutes are rounded to the nearest 15 minutes.

3. **Source**
/v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p4/body

4. **Notes**
The path was straightforward once at /v1/regions/attendance: the listing there explicitly flags `sec-hard-overtime` as "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01," which sits right next to superseded versions (`hard-overtime-v2`, and an `overtime-rate-table` referenced further back) and a `hard-overtime-legend-revision` file warning that overtime rate has three versions with different rules. It would be easy to grab the wrong-vintage row if scanning too fast — the current table's row address (`hard-overtime-row-day-d2-hours-h3-place-p4`) looks superficially similar to nothing else, but the surrounding superseded-version files are a trap for anyone not reading the "current since 2026-01-01" qualifier carefully. Row addresses are directly indexed by day/hours/place codes so once the D2/H3/P4 codes were known (they matched the question's own notation), locating the exact row was a single, unambiguous read — no need to consult the day/hours/place legends since the question already used the table's own D/H/P codes.
