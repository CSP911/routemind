1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "On a two-year contract, been here eight months, fully remote: monthly leave accrual and January cap" --member /v1/regions/attendance "accrual rates, remote-work leave rules, and carryover/cap details are likely here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_caf2c6 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l4/body

2. **Answer**:
Accrues 0.78 days per month. The carry-over limit is 7 days, so that is the most you can still be holding once the new year turns over into January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e2-tenure-t1-site-l4/body

4. **Notes**:
The legend-revision page was the thing to check first — the leave accrual subject has three versions (pre-2024-07-01, 2024-07-01–2025-12-31, and 2026-01-01-onward), and grabbing the newest table without checking would have been right here only by luck. Both "today" (2026-09-20) and "January" fall inside the 2026-01-01-onward window, so a single row (`sec-hard-accrual`) covers the whole question — no need to straddle two versions.

The three qualifiers ("two-year contract" → type E2, "eight months" → tenure T1, "fully from home" → site L4) each had a dedicated legend page with an explicit warning that the mapping is only written down there — guessing the codes from the question wording alone would have been a mistake, since e.g. "two-year contract" could easily be misread as a tenure detail rather than an employment-type one.

The only soft spot is interpreting "how much can I still be holding in January" as the carry-over limit (7 days) rather than a projected balance (accrual × months worked, capped at 7). The row's field is literally named "Carry-over limit, days," which reads as the ceiling on what can be held past year-end — that's the natural fit for the question as asked, but the document doesn't spell out a carryover *mechanism* (e.g., whether excess above the limit is forfeited automatically at year-end vs. some other date), so this is presented as the cap, not a guaranteed exact balance.
