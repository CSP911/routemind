1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p1/body

2. **Answer**
Multiplier: 1.68x. Minutes are rounded to the nearest 5 minutes.

3. **Source**
/v1/nodes/hard-overtime-row-day-d2-hours-h1-place-p1/body (primary answer)
/v1/nodes/hard-overtime-legend-revision/body (used to confirm the current, 2026-01-01-onward table is the right version for today's date)

4. **Notes**
The payroll area is a trap: it lists overtime-sounding content, but a warning note there says overtime premiums moved to attendance on 2026-01-01, with the payroll page itself flagged as the old, superseded rule. Going there first cost one extra hop but was worth it to rule it out explicitly rather than assume.

Within attendance, overtime rate has three historical versions (pre-2024-07-01, 2024-07-01 to 2025-12-31, and 2026-01-01 onward), each superseding the last without saying so. The legend-revision file was the only thing that made clear which version applies to today's date (2026-09-20) — without it, it would have been easy to grab the wrong version, especially since the older ones don't self-identify as replaced. The row itself was found directly by the day/hours/place code already given in the question (D2/H1/P1), so no legend lookup for day/hours/place codes was needed — the question already spoke in the table's own vocabulary.
