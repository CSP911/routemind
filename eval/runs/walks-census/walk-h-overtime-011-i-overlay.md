1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Tuesday, 3 hours at a client's office: what overtime multiplier applies, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime/work-hours rules likely live here" --member /v1/regions/payroll "overtime multiplier/pay rate likely defined here"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_f5e551 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p2/body

2. **Answer**
Multiplier: 1.35x. Rounding: to the nearest 10 minutes.

3. **Source**
/v1/nodes/hard-overtime-legend-revision/body (confirms 2026-09-20 falls under the current, 2026-01-01-onwards table)
/v1/nodes/hard-overtime-legend-day/body (an ordinary Tuesday → day D1)
/v1/nodes/hard-overtime-legend-hours/body (three hours → hours H2)
/v1/nodes/hard-overtime-legend-place/body (out at a client's office → place P2)
/v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p2/body (the answer row: multiplier 1.35x, rounding to the nearest 10 minutes)

4. **Notes**
The overtime table (`sec-hard-overtime`) is versioned three ways with a legend-revision page warning that "reaching for the newest is wrong for anything before 2026-01-01." Today's date (2026-09-20) is safely inside the current version's range, but I read the revision page before trusting the current table rather than assuming — the warning is explicit that the oldest version doesn't announce its own replacement, so skipping this check would have been the easy way to get a stale multiplier without any signal something was wrong.

The row lookup requires three separate legend translations (day, hours, place) before the actual row address can be built — none of the codes (D1/H2/P2) are guessable from the question text; each came from an explicit "what you have → what the rows call it" table. The day legend was the odd one out: three of its four entries are calendar day-types, but the fourth ("two in the morning" → D4) is a time-of-day, not a day — a reminder to actually read each row rather than pattern-match the column header.

The overlay close command reported all five addresses I used as "reached" rather than "used" — since I drilled into them via `table /v1/nodes/sec-hard-overtime` rather than adding them as overlay members first, they weren't names the overlay itself had printed. Functionally this didn't block anything; the answer was found and confirmed either way.
