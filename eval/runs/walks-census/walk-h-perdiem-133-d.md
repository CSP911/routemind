1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s4/body

2. **Answer**
Lodging cap: 219 USD per night. Receipt threshold: 58 USD — spend above this amount requires a receipt to be kept.
(For context, also in this row: meals 104 USD/day, incidentals 21 USD/day. An excess not pre-approved is settled at the table figure with the difference not recoverable; an unavoidable excess needs a short written statement plus evidence, decided by the budget holder.)

3. **Source**
/v1/nodes/hard-perdiem-row-grade-g2-band-b4-stay-s4/body

4. **Notes**
The grade/band/stay codes (G2, B4, S4) were given directly in the question, so the row address could be read straight off the sec-hard-perdiem table listing without needing the legend files (hard-perdiem-legend-grade/band/stay) that translate job titles, destination cities, or trip lengths into those codes — those would only be needed if the question had been phrased in plain terms instead of codes.

The expense region table flags that overseas per-diem has three versions (a warning file, hard-perdiem-legend-revision) and lists both a superseded v2 table (hard-perdiem-v2, in force 2024-07-01 to 2025-12-31) and the current one (sec-hard-perdiem, in force from 2026-01-01) side by side. It would be easy to grab the wrong version's row if not reading the "current table since 2026-01-01" note carefully — today's date (2026-09-20) falls under the current table, which is the one used here.
