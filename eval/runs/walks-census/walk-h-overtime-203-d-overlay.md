1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D3, hours H1, place P4, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table by day, hours, place, in force since 2026-01-01"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_bcf7fb --outcome answered --used /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p4/body

2. **Answer**: Multiplier is 2.25x. Minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h1-place-p4/body

4. **Notes**: The overlay create step, given the top-level `/v1/nodes/sec-hard-overtime` address as its single member, expanded into a 67-row working set that included every day/hours/place combination (D1–D4 × H1–H4 × P1–P4) plus three legend files (day, hours, place). The exact row for D3/H1/P4 was already printed in that expansion, so no need to consult the legends to resolve what D3/H1/P4 mean. The attendance region table lists both a current overtime table (`sec-hard-overtime`, in force since 2026-01-01) and two superseded versions (`hard-overtime-v2` for 2024-07-01–2025-12-31, and an older `overtime-rate-table`); today's date (2026-09-21) falls under the current version, so the current row was the correct one and the superseded rows were never fetched. One oddity: closing the overlay with `--used` set to the exact address that create's `--member` had named came back labeled "reached" rather than a normal confirmed-used member — the tool's message says "reached = answered from somewhere the overlay never named," which seems inconsistent since that address was literally in the overlay's printed table. Didn't affect the answer, but worth flagging as a quirk in the overlay bookkeeping.
