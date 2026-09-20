1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p3/body

2. **Answer**: Multiplier is 1.74x; minutes are rounded to the nearest 5 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p3/body

4. **Notes**: The attendance area lists both a current and two superseded overtime tables (`hard-overtime-v2` for 2024-07-01 to 2025-12-31, and an older `overtime-rate-table`), plus a legend-revision note flagging three versions total. Today's date (2026-09-20) falls under the current table `sec-hard-overtime`, in force since 2026-01-01, so that's the one used — it would have been easy to grab a superseded version by mistake if the "in force from" dates weren't checked. Once inside `sec-hard-overtime`, the row for day D2/hours H1/place P3 was listed explicitly by exact address, so no legend lookups (day/hours/place definitions) were needed to resolve the question as asked.
