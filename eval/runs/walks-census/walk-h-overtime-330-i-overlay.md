1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "2am, 11 hours, at desk: overtime multiplier and minute rounding" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01" --member /v1/nodes/hard-overtime-legend-revision/body "warns overtime rate has three versions with different date ranges - need to confirm which applies to today 2026-09-21"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p1/body
./bench/rmcli.py overlay add --id ov_2026-09-21_5f9ad7 --address /v1/nodes/hard-overtime-legend-day/body --why "maps 'two in the morning' to day D4"
./bench/rmcli.py overlay add --id ov_2026-09-21_5f9ad7 --address /v1/nodes/hard-overtime-legend-hours/body --why "maps 'eleven hours' to hours H4"
./bench/rmcli.py overlay add --id ov_2026-09-21_5f9ad7 --address /v1/nodes/hard-overtime-legend-place/body --why "maps 'at my desk' to place P1"
./bench/rmcli.py overlay add --id ov_2026-09-21_5f9ad7 --address /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p1/body --why "the row for D4/H4/P1: multiplier and rounding"
./bench/rmcli.py overlay close --id ov_2026-09-21_5f9ad7 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p1/body

2. **Answer**
Multiplier: 3.00x. Rounding: to the nearest 20 minutes.

3. **Source**
/v1/nodes/hard-overtime-legend-revision/body
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p1/body

4. **Notes**
The tempting first read of "day D1/D2/D3/D4" is weekday/weekend/holiday, since the legend's first three rows are "an ordinary Tuesday," "a Saturday," "Liberation Day" — calendar day types. The question gives no calendar date at all, only a clock time ("two in the morning"), so it looked at first like the day-type qualifier might be unanswerable from the question. But the legend's fourth row is literally "two in the morning → day D4" — the table isn't purely calendar-day-of-week, it also uses clock time as a day-type qualifier, and the wording of the question matches that row verbatim. That's the one place I nearly went wrong: assuming the question was missing a required qualifier when it was actually giving it in a different form than the other three rows implied.

The other point worth flagging: the revision-warning page states three versions of this table exist with different date ranges, and explicitly warns against always reaching for the newest. Today (2026-09-21) falls after 2026-01-01, so the current table (`sec-hard-overtime`) is correct here, but that had to be checked rather than assumed, per the warning page itself.

The three qualifiers (day, hours, place) each matched a legend row exactly on the given wording ("eleven hours" → H4, "at my desk" → P1), so no nearest-entry judgment call was needed for those two.
