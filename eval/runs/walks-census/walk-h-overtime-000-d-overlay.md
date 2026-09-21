1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D1, hours H1, place P1, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place - matches D1/H1/P1 axes"
./bench/rmcli.py overlay remove --id ov_2026-09-20_dcd107 --address /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p2/body --why "wrong place"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p1/body
./bench/rmcli.py overlay close --id ov_2026-09-20_dcd107 --outcome answered --used /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p1/body

2. **Answer**: Multiplier 1.20x; minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p1/body

4. **Notes**: The row I needed matched the question's own D1/H1/P1 labels almost literally, so this walk went straight through — table list → attendance region → the current overtime table (`sec-hard-overtime`, in force from 2026-01-01, explicitly marked as superseding two older versions) → the exact row. The one place I nearly fumbled: I tried to `remove` a neighboring row (place P2) from the overlay to tidy the working set, and the CLI rejected it with a 404, saying that address was never a member — even though the overlay listing had printed all 67 leaf rows under `sec-hard-overtime` right after creation. That listing is apparently just a preview of what's reachable under the member I added (the table `sec-hard-overtime`), not a set of individually-addable/removable members itself. Consistent with that, closing the overlay with the exact row I used came back marked "reached" rather than a plain match — the tool's way of saying I answered from something the overlay named as a browsable child, not as a directly-added member. Worth remembering: adding a table as a member does not make its children individually removable members. Also worth noting the domain has old superseded overtime tables (`hard-overtime-v2`, and one before that) — the "which version is current" legend/warning file made it clear 2026-01-01 is the right cutover date for today (2026-09-20/21), so I didn't need to check those older versions.
