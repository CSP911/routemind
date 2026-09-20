1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p4/body

2. **Answer**: Multiplier 2.13x; minutes are rounded to the nearest 20 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h4-place-p4/body

4. **Notes**: The `/v1/nodes/sec-hard-overtime` table lists 64 rows (D1–D4 × H1–H4 × P1–P4) plus separate legend files for day/hours/place codes. The question already gave the codes (D2/H4/P4) directly, so I went straight to the matching row rather than resolving the legends — worth flagging in case "D2/H4/P4" in the question weren't meant as the literal codes used in this table. The row's own header confirmed it's from the current table (in force since 2026-01-01, current as of today 2026-09-20); the area listing had also flagged that an older superseded version (`hard-overtime-v2`, 2024-07-01 to 2025-12-31) and a version before that (`overtime-rate-table`) exist under the same day/hours/place shape, so picking the wrong table here would have silently given a plausible-looking but outdated multiplier and rounding rule.
