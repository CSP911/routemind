1. **Commands**
```
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/expense
./bench/rmcli.py table /v1/nodes/sec-hard-perdiem
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-grade/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-band/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-stay/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s1/body
./bench/rmcli.py read /v1/nodes/hard-perdiem-legend-revision/body
```

2. **Answer**
Lodging cap: 335 USD per night. Receipt required for any spend above 57 USD.
(Also on this row, not asked but adjacent: meals 107 USD/day, incidentals 22 USD/day.)

3. **Source**
- /v1/nodes/hard-perdiem-legend-grade/body (managing director → grade G4)
- /v1/nodes/hard-perdiem-legend-band/body (Dhaka → band B4)
- /v1/nodes/hard-perdiem-legend-stay/body (one night → stay S1)
- /v1/nodes/hard-perdiem-row-grade-g4-band-b4-stay-s1/body (the figures)
- /v1/nodes/hard-perdiem-legend-revision/body (confirms today's date, 2026-09-20, falls under the current table, not the two superseded versions)

4. **Notes**
The expense region table flags up front that overseas per-diem has three superseded/current versions living side by side, with a dedicated warning node (`hard-perdiem-legend-revision`) whose whole point is that the oldest version never says it was replaced — reaching for whichever result looks newest or most complete would be wrong for a question dated in 2025. Today's date (2026-09-20) is safely inside the current table's range (2026-01-01 onwards), so this wasn't actually ambiguous here, but it's the kind of question where guessing the version instead of checking would have produced a plausible but wrong number. The three legends (grade/band/stay) are also easy to skip if you go straight for a row address — the row table gives no hint which of the 64 rows applies without them, and none of it is guessable (e.g. Dhaka is band B4, not obviously tied to any real-world tier ordering).
