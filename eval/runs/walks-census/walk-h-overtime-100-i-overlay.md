1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Saturday, about ninety minutes, at desk: what multiplier applies, and to what rounding are minutes taken?" --member /v1/regions/attendance "overtime/weekend work rules likely live here" --member /v1/regions/payroll "overtime pay multiplier and rounding could be a payroll policy"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f11324 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p1/body

2. **Answer**: Multiplier 1.68x. Minutes are rounded to the nearest 5 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p1/body

4. **Notes**: The overtime rate subject has three superseded versions with overlapping validity windows, and the legend-revision page explicitly warns that the oldest version says nothing about being replaced — so it's easy to grab the wrong one if you don't check it first. Today's date (2026-09-20/21) falls after the 2026-01-01 cutoff, so the current table (`sec-hard-overtime`) is correct, but this is exactly the kind of question where guessing "the current one is always right" would coincidentally work here while being the wrong instinct for a question dated in 2025. The three qualifiers (day/hours/place) each had their own legend requiring translation from the plain-English question into codes (Saturday→D2, ~90 minutes→H1, at my desk→P1) before the specific row address could be constructed from the table's own listing — I did not guess the address, I picked it from the printed row list after resolving all three codes. No ambiguity in the final row itself.
