1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p4/body

2. **Answer**: Multiplier 2.13x; minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p4/body

4. **Notes**: The attendance region listed both a current overtime table (`sec-hard-overtime`, in force since 2026-01-01) and two superseded versions (`hard-overtime-v2`, `overtime-rate-table`), each with their own body pages appearing right alongside the current table's node in the attendance listing — easy to grab the wrong one if not reading the "in force" dates carefully. Since today is 2026-09-20, the current table applies. The row addresses use codes (D2/H4/P4) rather than plain words, so all three legends had to be read first to translate "a Saturday", "eleven hours", and "from home" into the right codes before the specific row address could be used — the tool warns not to construct addresses, and indeed the legends were the only place the day/hours/place codes were defined.
