1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p1/body

2. **Answer**: Multiplier 1.32x; minutes rounded to the nearest 10 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d1-hours-h2-place-p1/body

4. **Notes**: The payroll area's own overtime page (`hard-moved-overtime`) explicitly redirects to attendance, since the rates moved there on 2026-01-01 — checking payroll first wasn't wasted, it confirmed the current owner of the fact. The real trap is the "current table" table itself: it's indexed by day/hours/place codes (D1–D4, H1–H4, P1–P4) with no plain-language row, so the three legend files are mandatory reading, not optional context — skipping them would make it impossible to pick the right one of 64 rows. Each legend maps phrases almost verbatim to the question's wording ("an ordinary Tuesday" → D1, "three hours" → H2, "at my desk" → P1), so there was no ambiguity in this case, but the legends' own fallback instruction ("take the nearest entry above it") is a warning that other phrasings could require a judgment call I didn't have to make here. Also worth flagging: this table is the *current* one only because today (2026-09-20) falls after the 2026-01-01 effective date — the region page notes two superseded versions (`hard-overtime-v2`, `overtime-rate-table`) that would apply to a question about an earlier date.
