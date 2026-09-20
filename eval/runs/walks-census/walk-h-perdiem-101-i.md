1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s2/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body

2. **Answer**
For a team manager (grade G2) on a four-night trip (stay S2) to Tokyo (band B1), under the current overseas per-diem table (in force 2026-01-01 onward, which covers today, 2026-09-20):
- Lodging cap: 163 USD per night
- Receipt threshold: 25 USD — spend above this amount requires the receipt to be kept
(Also on this row, though not asked: meals 52 USD/day, incidentals 10 USD/day.)

3. **Source**
/v1/nodes/hard-perdiem-legend-grade/body
/v1/nodes/hard-perdiem-legend-band/body
/v1/nodes/hard-perdiem-legend-stay/body
/v1/nodes/hard-perdiem-row-grade-g2-band-b1-stay-s2/body
/v1/nodes/hard-perdiem-legend-revision/body (used to confirm the current table, not an older version, applies to today's date)

4. **Notes**
The expense area table warns up front that overseas per-diem has three versions ("the older band-only caps are still here and are superseded"), and the /v1/nodes/sec-hard-perdiem table listing repeats that warning. It would have been easy to grab the first per-diem-looking row without checking dates. The legend-revision doc makes clear the date on the question decides the version — the oldest doc "says nothing at all about having been replaced," so date-checking can't be skipped. Today (2026-09-20) clearly falls under the current table (2026-01-01 onward), so no ambiguity there, but the trap is real for questions dated in 2025 or earlier.

The three legends (grade, band, stay) had to be resolved before the correct one of 64 rows could be addressed — none of the rows are guessable from job title, city, or trip length directly; each required a separate lookup ("a team manager" → G2, "Tokyo" → B1, "four nights" → S2, matched exactly in the stay legend so no nearest-entry judgment call was needed).
