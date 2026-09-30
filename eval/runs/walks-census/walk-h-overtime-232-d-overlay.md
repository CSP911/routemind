1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "For day D3, hours H4, place P3, what multiplier applies to that time, and to what rounding are the minutes taken?" --member /v1/nodes/sec-hard-overtime "current overtime rate table, in force from 2026-01-01, by day/hours/place"
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p3/body
./bench/rmcli.py overlay close --id ov_2026-09-21_e69b3a --outcome answered --used /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p3/body

2. **Answer**: Multiplier is 2.58x; minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d3-hours-h4-place-p3/body

4. **Notes**: Opening the overlay member /v1/nodes/sec-hard-overtime expanded into 67 individual per-day/hour/place row files plus three legend files (day, hours, place). Because the question already specified all three qualifiers (D3, H4, P3) exactly, the matching row address was directly visible in that expansion and could be read without consulting the legends to resolve ambiguity. Worth flagging: on close, the tool reported the used address as "reached ... answered from somewhere the overlay never named" — I had added only the parent table /v1/nodes/sec-hard-overtime as an overlay member, not the specific row file, so the row I actually read was never formally added as a member even though it appeared in the overlay's printed listing. No real ambiguity in this walk otherwise; the table naming (D3/H4/P3) maps one-to-one to an address, so there was no risk of picking the wrong row.
