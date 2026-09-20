1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p3/body

2. **Answer**: Multiplier 2.10x; minutes rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p3/body

4. **Notes**: The table is indexed by codes (D/H/P), not by the plain-language terms in the question, so all three legends had to be read first to translate "a Saturday" → D2, "eleven hours" → H4, and "on standby at home" → P3 before the right row could be addressed — there was no way to jump straight to the row. The legend tables warn to "take the nearest entry above" for unlisted values, but all three of this question's terms ("a Saturday", "eleven hours", "on standby at home") matched a legend row exactly, so no approximation was needed. Also worth flagging: there is a superseded version of this table (`hard-overtime-v2`, in force 2024-07-01 to 2025-12-31) and an even older `overtime-rate-table`; it would be easy to grab a row from one of those by mistake. I used `sec-hard-overtime`, explicitly marked as the current table in force from 2026-01-01, which matches today's date (2026-09-20).
