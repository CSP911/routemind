1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l4/body

2. **Answer**:
For type E1, tenure T3, site L4 (current table, in force since 2026-01-01): you accrue 0.62 days of leave per month. The carry-over limit is 13 days — that is the most you can still be holding when the balance is checked in January.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body (confirmed which of the three accrual table versions applies to today's date, 2026-09-20 — the current one)
/v1/nodes/hard-accrual-row-type-e1-tenure-t3-site-l4/body (the accrual rate and carry-over limit figures)

4. **Notes**:
The attendance area lists three separate leave-accrual documents (`leave-accrual`, `hard-accrual-v2`, `sec-hard-accrual`) with a warning that the oldest one never states it was superseded. It would have been easy to grab the first accrual-looking table without checking the legend-revision page first. Today's date (2026-09-20) falls after 2026-01-01, so the current table (`sec-hard-accrual`) is correct, but this required a deliberate date check rather than just picking the top or most-detailed-looking hit.

The row itself directly matched the question's codes (E1, T3, L4) with no need to translate via the site/tenure/type legends, since the question was already phrased in those exact codes — but I did not independently verify via the legends that "E1/T3/L4" was the right code set for a plain-language description, since none was given. The row's "Carry-over limit, days" field was the best match for "how much can I still be holding in January" — there was no separate, January-specific cap document, so I'm treating the carry-over limit as the answer to that half of the question. That inference is reasonable but not spelled out verbatim in the source as being specifically a "January" figure.
