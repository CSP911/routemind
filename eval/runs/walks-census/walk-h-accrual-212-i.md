1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l3/body

2. **Answer**
Accrues 1.16 days per month. Carry-over limit is 9 days — that is the most that can still be held (into January, or at any point).

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body (confirms today's date, 2026-09-20, falls under the current table, not the two older versions)
/v1/nodes/hard-accrual-legend-type/body (maps "three days a week" → type E3)
/v1/nodes/hard-accrual-legend-tenure/body (maps "been here two years" → tenure T2)
/v1/nodes/hard-accrual-legend-site/body (maps "Singapore entity" → site L3)
/v1/nodes/hard-accrual-row-type-e3-tenure-t2-site-l3/body (the figures: 1.16 days/month accrual, 9-day carry-over limit)

4. **Notes**
- The legend-revision page exists specifically to stop you from grabbing the newest accrual table by reflex. Today's date (2026-09-20) is after 2026-01-01, so the current table (`sec-hard-accrual`) is correct here — but this is the one place in the walk where guessing instead of checking would have accidentally been right, which is worse than checking, since a question dated a year earlier would need the superseded `hard-accrual-v2` instead.
- The type legend has a trap built for this exact question: "on a two-year contract" is mapped to type E2. The question says "in three days a week" for employment type and separately "been here two years" for tenure — those are two different qualifiers (type vs. tenure) that happen to share the word "two years." It would be easy to misread "two years" as selecting E2 (the two-year-contract type) instead of using it for tenure and taking "three days a week" for type (E3). I used three days a week → E3 for type and two years → T2 for tenure, kept separate.
- "How much can I still be holding in January" reads like it could mean something special about the January payroll/settlement cycle, but nothing in the row or the attendance table ties carry-over specifically to January — the carry-over limit (9 days) is just the standing cap on how much leave balance can be held at any time, and I found no January-specific rule anywhere in this walk. Answered it as the carry-over limit; flagging in case a January-specific provision exists elsewhere that this walk didn't surface.
