1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Saturday, three hours, on standby at home: what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/regions/payroll "overtime multipliers and pay rules are typically documented here" --member /v1/regions/attendance "standby/on-call and Saturday work classification may be defined here"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_1c5d4f --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p3/body

2. **Answer**
Multiplier: 1.86x. Rounding: to the nearest 10 minutes.

3. **Source**
/v1/nodes/hard-overtime-legend-revision/body (confirmed the 2026-01-01 table is the version in force for a 2026-09-20 question)
/v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
/v1/nodes/hard-overtime-legend-hours/body (three hours → hours H2)
/v1/nodes/hard-overtime-legend-place/body (on standby at home → place P3)
/v1/nodes/hard-overtime-row-day-d2-hours-h2-place-p3/body (the answer: 1.86x, rounded to the nearest 10 minutes)

4. **Notes**
The overtime rate subject has three superseded/current versions indexed by different numbers of qualifiers, and the legend-revision page warns explicitly that reaching for the newest version is wrong for dates before 2026-01-01 — I checked that page first before touching the row table, since today's date (2026-09-20) made the current table the right pick but that isn't obvious without reading the warning. The place legend was the easy spot to slip: "on standby at home" and "from home" are two distinct codes (P3 vs P4) sitting right next to each other, and a careless read could have picked P4 since the question says "at home." The wording "on standby at home" matches P3 exactly, so no ambiguity once read carefully, but it's the kind of near-miss worth flagging. Everything else — day and hours legends — mapped cleanly with exact phrase matches ("a Saturday" → D2, "three hours" → H2).
