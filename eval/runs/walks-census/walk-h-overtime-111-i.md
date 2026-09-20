1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p2/body
```

2. **Answer**
Multiplier: 1.83x. Rounding: to the nearest 10 minutes.

3. **Source**
- /v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
- /v1/nodes/hard-overtime-legend-hours/body (three hours → hours H2)
- /v1/nodes/hard-overtime-legend-place/body (out at a client's office → place P2)
- /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p2/body (multiplier and rounding)

4. **Notes**
The attendance table lists three superseded/current overtime documents (`hard-overtime-v2`, `overtime-rate-table`, and the current `sec-hard-overtime`), each with its own "WARNING" revision-legend file. It would have been easy to grab a row from the wrong version — the row addresses across versions likely look similar (day/hours/place codes), so I made sure to open the table explicitly marked "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01" and confirmed 2026-09-20 falls inside that range before reading any row. The three legends (day, hours, place) had to be read separately and combined into a single D2-H2-P2 address by hand — the tool never builds this address for you, so a slip in any one of the three codes would silently point at the wrong row.
