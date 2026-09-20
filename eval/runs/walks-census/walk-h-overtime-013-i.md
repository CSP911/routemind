1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p4/body

2. **Answer**
Multiplier: 1.41x. Rounding: to the nearest 10 minutes.
(Day D1 = "an ordinary Tuesday", Hours H2 = "three hours", Place P4 = "from home".)

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p4/body

4. **Notes**
Straightforward walk once the current table was found. The attendance area listed both a current
overtime table (`sec-hard-overtime`, in force from 2026-01-01) and two superseded versions
(`hard-overtime-v2`, `overtime-rate-table`) plus a legend-revision note — easy to grab a stale
version by mistake if you don't read the "current table since 2026-01-01" framing in the
attendance table's description. The three legends (day/hours/place) each warn that unlisted
inputs should use "the nearest entry above," but the question's inputs ("an ordinary tuesday",
"three hours", "from home") matched legend rows exactly, so no interpolation was needed. No
ambiguity in the final row itself.
