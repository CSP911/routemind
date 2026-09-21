1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Saturday, about ninety minutes, at a client's office: what multiplier applies, and to what rounding are the minutes taken?" --member /v1/regions/attendance "overtime application, hours worked, rounding rules likely live here" --member /v1/regions/payroll "overtime multiplier/pay rate likely explained as a payslip line item"
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p2/body
./bench/rmcli.py overlay close --id ov_2026-09-20_ceaf82 --outcome answered --used /v1/nodes/sec-hard-overtime /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body /v1/nodes/hard-overtime-legend-place/body /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p2/body

2. **Answer**
Multiplier: 1.71x. Rounding: to the nearest 5 minutes.
(This is the current table, in force from 2026-01-01; today is 2026-09-21, so this version applies.)

3. **Source**
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p2/body

4. **Notes**
The overtime rate table is indexed by three codes (day/hours/place), each translated by its own legend — the answer isn't in one document, it's the intersection of four. Easy to go wrong two ways: (1) picking the wrong overtime version — there's a `hard-overtime-legend-revision` warning that the rate has three superseded versions, and I had to trust that "the current table" (`sec-hard-overtime`, in force 2026-01-01 onward) was correct for today's date (2026-09-21) rather than grabbing an older `hard-overtime-v2` row by mistake; (2) the legends explicitly say to take the nearest entry if the exact wording isn't listed — "about ninety minutes" matched H1 ("about ninety minutes") verbatim, "a Saturday" matched D2 verbatim, and "out at a client's office" matched P2 verbatim, so no fuzzy-matching judgment call was actually needed here, but I checked all three legends fully before assuming that.

One oddity: my overlay only had the region-level tables (`/v1/regions/attendance`, `/v1/regions/payroll`) as members, not the specific leaf addresses I ended up reading. Closing with `--used` on the leaf addresses came back marked "reached" rather than a clean match, since I never formally added them as overlay members — worth doing `overlay add` for the intermediate/leaf nodes next time before closing, to keep the overlay's own record aligned with what was actually used.
