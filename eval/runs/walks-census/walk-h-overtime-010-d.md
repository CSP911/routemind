1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p1/body

2. **Answer**: Multiplier is 1.32x; minutes are rounded to the nearest 10 minutes.

3. **Source**: /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p1/body

4. **Notes**: Straightforward walk. `/v1/regions/attendance` listed both a current table (`sec-hard-overtime`, in force from 2026-01-01) and a superseded one (`hard-overtime-v2`, 2024-07-01 to 2025-12-31) — worth noting because picking the wrong version would silently give the wrong multiplier. Since today's date (2026-09-20) falls within the current table's validity window, `sec-hard-overtime` was the correct choice, confirmed by its own listing explicitly saying "THE CURRENT OVERTIME RATE TABLE, in force from 2026-01-01." The row address matched the day/hours/place codes (D1, H2, P1) exactly as given in the question, so no legend lookups were needed to translate plain-language qualifiers into codes.
