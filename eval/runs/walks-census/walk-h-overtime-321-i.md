1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/payroll
./bench/rmcli.py read /v1/nodes/hard-moved-overtime/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-overtime
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-day/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-hours/body
./bench/rmcli.py read /v1/nodes/hard-overtime-legend-place/body
./bench/rmcli.py read /v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p2/body

2. **Answer**
Multiplier: 2.91x. Rounding: to the nearest 15 minutes.

3. **Source**
/v1/nodes/hard-moved-overtime/body (established payroll's old rule no longer applies as of 2026-01-01, today being 2026-09-20)
/v1/nodes/hard-overtime-legend-revision/body (confirmed the current, three-qualifier table is the right version for today's date)
/v1/nodes/hard-overtime-legend-day/body (maps "two in the morning" → day D4)
/v1/nodes/hard-overtime-legend-hours/body (maps "six hours" → hours H3)
/v1/nodes/hard-overtime-legend-place/body (maps "out at a client's office" → place P2)
/v1/nodes/hard-overtime-row-day-d4-hours-h3-place-p2/body (the answer: 2.91x, rounding to the nearest 15 minutes)

4. **Notes**
The natural first stop was payroll, since overtime pay used to live there — but that page is dated and now just redirects to attendance's `sec-hard-overtime`, effective 2026-01-01. That redirect could easily be missed if the payroll table's overtime-sounding entries (`payslip-overtime`, `sec-pay-structure-and-review`) were opened directly without reading the payroll table's own header warning first.

Once in attendance, there's a legend-revision warning that the overtime table has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01 onward) indexed by one, two, and three qualifiers respectively. Since today is 2026-09-20, the current three-qualifier table (`sec-hard-overtime`) is correct — but it would be an easy trap to grab the two-qualifier `hard-overtime-v2` by habit or to assume "current" without checking the in-force date against today's date.

The biggest trap was the day legend. "Two in the morning" is not a day-of-week concept at all — it's listed directly as day D4 in the day-type legend, sitting alongside "an ordinary Tuesday," "a Saturday," and "Liberation Day." It would be very easy to think the question is missing information (what day of the week is it?) and either guess a day or treat "two in the morning" as only relevant to the hours legend. It isn't in the hours legend at all; it's purely a day-code qualifier, and "six hours" is the separate hours qualifier (H3). Missing this would have led to picking the wrong row or concluding the question was unanswerable.
