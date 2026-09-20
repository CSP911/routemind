1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p4/body

2. **Answer**: Multiplier 1.29x; minutes are rounded to the nearest 5 minutes. (Current table, in force from 2026-01-01.)

3. **Source**:
/v1/nodes/hard-overtime-row-day-d1-hours-h1-place-p4/body

4. **Notes**: Payroll's table front matter warned that overtime/night/holiday premium rates moved to attendance on 2026-01-01, so the real risk here was answering from the stale payroll page (`/v1/nodes/hard-moved-overtime`) instead of following the pointer to attendance. Inside attendance, `sec-hard-overtime` is explicitly flagged as THE CURRENT table (vs. superseded `hard-overtime-v2` and `overtime-rate-table`), and it happened to have a row pre-indexed exactly as "day-d1-hours-h1-place-p4," so no legend lookup was needed to translate D1/H1/P4 into codes — the question already used the table's own code names. Only real risk of error was reading `hard-overtime-v2` (the 2024-07-01–2025-12-31 superseded version) by mistake since it's listed right next to the current table in the same directory listing.
