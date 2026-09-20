1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p4/body

2. **Answer**: Multiplier 3.09x. Minutes are rounded to the nearest 20 minutes.

3. **Source**:
/v1/nodes/hard-overtime-legend-day/body
/v1/nodes/hard-overtime-legend-hours/body
/v1/nodes/hard-overtime-legend-place/body
/v1/nodes/hard-overtime-row-day-d4-hours-h4-place-p4/body

4. **Notes**: The "day" legend is not weekday/weekend/holiday as the row-index names (D1–D4) suggest — it's a grab-bag mapping arbitrary example inputs to codes, and "two in the morning" maps to D3 by conventional understanding of it being an anomaly. However the legend table literally lists "two in the morning" as its own row mapping to D4, distinct from "an ordinary Tuesday" (D1), "a Saturday" (D2), and "Liberation Day" (D3) — so the question's time-of-day clause is actually the day-code qualifier, not a hint about night-shift hours. This was the easiest place to go wrong: I almost read "two in the morning" as flavor text for late-night overtime and looked for a night differential elsewhere, instead of matching it verbatim against the day legend. Also had to confirm the current (2026-01-01-forward) overtime table applied rather than the superseded `hard-overtime-v2` — today's date (2026-09-20) falls under `sec-hard-overtime`, so no cross-version reconciliation was needed. The three legends (day/hours/place) had to be resolved independently and then combined into a single row address (d4-h4-p4) — the table listing gives no shortcut for this, each qualifier must be looked up on its own before the row address can be assembled.
