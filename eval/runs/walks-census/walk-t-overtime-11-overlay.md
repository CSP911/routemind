1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py overlay create --question "What multiplier was paid for ordinary overtime beyond the 40-hour week in 2023, and what had it become by 2025?" --member /v1/nodes/hard-moved-overtime/body "payroll page notes overtime premiums moved to attendance 2026-01-01; this old page may hold historical rates" --member /v1/regions/attendance "overtime rates now live here per payroll's redirect note"
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py read /v1/nodes/hard-overtime-v2/body
./bench/rmcli.py read /v1/nodes/overtime-rate-table/body
./bench/rmcli.py table /v1/nodes/sec-overtime-and-hours
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py table /v1/nodes/hard-overtime-v2
./bench/rmcli.py overlay add --id ov_2026-09-20_b2de70 --address /v1/nodes/hard-overtime-legend-revision/body --why "confirms which of the three overtime rate versions applies to 2023 vs 2025"
./bench/rmcli.py overlay add --id ov_2026-09-20_b2de70 --address /v1/nodes/overtime-rate-table/body --why "oldest version (until 2024-07-01), covers 2023: ordinary overtime beyond 40hr week = +50%"
./bench/rmcli.py overlay add --id ov_2026-09-20_b2de70 --address /v1/nodes/hard-overtime-legend-day/body --why "defines day code D1 = an ordinary weekday, needed to pick the right cell in the v2 grid"
./bench/rmcli.py overlay add --id ov_2026-09-20_b2de70 --address /v1/nodes/hard-overtime-legend-hours/body --why "defines hours code H1 = about ninety minutes, the entry band, needed to pick the right cell in the v2 grid"
./bench/rmcli.py overlay remove --id ov_2026-09-20_b2de70 --address /v1/nodes/hard-moved-overtime/body --why "navigational redirect only, not a source of the answer"
./bench/rmcli.py overlay close --id ov_2026-09-20_b2de70 --outcome answered --used /v1/nodes/hard-overtime-legend-revision/body /v1/nodes/overtime-rate-table/body /v1/nodes/hard-overtime-v2/body /v1/nodes/hard-overtime-legend-day/body /v1/nodes/hard-overtime-legend-hours/body

2. **Answer**:
- 2023: +50% (1.5x) for ordinary overtime beyond the 40-hour week — a single flat rate, not split by day or hour band.
- 2025: 1.20x — the entry-band figure from the day/hours grid (D1 = an ordinary weekday, H1 = the first hour band, ~90 minutes) that replaced the flat rate on 2024-07-01. The 2025 rule is no longer a single number: the v2 grid runs from 1.20x (D1/H1, ordinary weekday, first band) up to 1.65x (D4/H4), varying by day type and hours worked. 1.20x is the base/ordinary cell; heavier days or longer overtime stretches in 2025 paid more than that.

3. **Source** (in order used):
- /v1/nodes/hard-overtime-legend-revision/body — established that 2023 needs the oldest table and 2025 needs the v2 table, not the current one.
- /v1/nodes/overtime-rate-table/body — the 2023 (pre-2024-07-01) flat rate: +50%.
- /v1/nodes/hard-overtime-v2/body — the 2024-07-01–2025-12-31 grid, giving the 2025 figures including the 1.20x base cell.
- /v1/nodes/hard-overtime-legend-day/body — decoded day code D1 as an ordinary weekday.
- /v1/nodes/hard-overtime-legend-hours/body — decoded hours code H1 as the first (shortest) overtime band.

4. **Notes**:
Payroll's own overtime page (`hard-moved-overtime`) just redirects to attendance as of 2026-01-01 and holds no rates itself — a dead end I checked first because payroll seemed the obvious home for a pay multiplier. The real trap was `sec-hard-overtime`, printed at the top of the attendance table as "THE CURRENT OVERTIME RATE TABLE" — reaching for it would have answered with the 2026-onward rule, which is wrong for both 2023 and 2025. `hard-overtime-legend-revision` explicitly warns against exactly this ("reaching for the newest is wrong for anything before 2026-01-01"), and states 2025 needs the *middle* version, not the newest — that warning is the reason I didn't just grab `sec-hard-overtime`.
A second ambiguity: the 2025 rule (v2) isn't a single multiplier — it's an 4x4 grid by day type and hour band, unlike 2023's flat +50%. The question asks for "the multiplier" as if there's one number, so I read the legend-day/legend-hours files (which live under the *current*, three-qualifier table, `sec-hard-overtime`) to confirm D1/H1 means "an ordinary weekday, first hour band" — the closest match to "ordinary overtime beyond the 40-hour week." Those legend files aren't duplicated under `hard-overtime-v2` itself, so I'm inferring the day/hour vocabulary is shared across versions (the v2 page's own text — "the multiplier... followed the overtime rates rule unchanged until 2026-01-01" — supports this, but it isn't spelled out as explicitly as I'd like). I reported the full grid range in the answer so the single-cell pick doesn't hide the fact that 2025 rates varied by day and duration where 2023's didn't.
