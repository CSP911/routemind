1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p4/body

2. **Answer**: Multiplier 2.01x. Minutes are rounded to the nearest 15 minutes.

3. **Source**:
/v1/nodes/sec-hard-overtime (table, to find the legends and rows)
/v1/nodes/hard-overtime-legend-day/body (Saturday → day D2)
/v1/nodes/hard-overtime-legend-hours/body (six hours → hours H3)
/v1/nodes/hard-overtime-legend-place/body (from home → place P4)
/v1/nodes/hard-overtime-row-day-d2-hours-h3-place-p4/body (the answer)

4. **Notes**: The attendance table lists three versions of the overtime rate: a current table (`sec-hard-overtime`, in force since 2026-01-01), a superseded v2 (2024-07-01 to 2025-12-31), and an older `overtime-rate-table`. Since today is 2026-09-20, the current table is the correct one — it would be easy to grab the wrong version by mistake if the "WHY" summaries weren't read carefully. The three qualifiers (day, hours, place) each needed their own legend lookup — none of the values ("Saturday", "six hours", "from home") are usable directly as an address component; they had to be translated to D2/H3/P4 first via the three separate legend files before the single matching row could be addressed. "From home" (P4) also had to be distinguished from the similar-sounding "on standby at home" (P3) in the place legend — easy to conflate if skimming.
