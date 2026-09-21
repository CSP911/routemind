1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner firm employee, 9 years tenure, Singapore entity: monthly leave accrual rate and max carry-forward/cap holdable in January?" --member /v1/regions/attendance "leave accrual, tenure-based rates, and carry-forward caps live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7bcb59 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l3/body

2. **Answer**:
Accrues 1.64 days per month. Carry-over limit (the most you can still be holding when January starts) is 15 days.

3. **Source**:
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t4-site-l3/body

4. **Notes**:
Leave accrual has three superseded/current versions gated by date (legend-revision made this explicit and warns not to reach for the newest reflexively). Today (2026-09-20/21) falls after 2026-01-01, so the current table `sec-hard-accrual` was the correct pick — but this is exactly the kind of question where grabbing the newest table without checking the date would coincidentally have been right, which is a bad habit to reinforce; I read the revision legend first specifically to confirm it rather than assume it.

The three qualifiers (type/tenure/site) are each phrase-matched against a legend, not obvious from the question's wording. "Here from our partner firm" maps to type E4, which is a literal near-quote of the question's own phrasing in the legend — easy to grab correctly, but it would have been easy to instead guess "contractor" or "vendor" type reasoning if the legend hadn't used the same words. "Nine years" landed exactly on tenure T4 ("been here nine years") with no banding ambiguity. "Singapore entity" was the only site legend entry not phrased as a physical office ("Seoul office", "Busan branch") but as an entity — still an unambiguous match to L3.

The question's second half, "how much can I still be holding in January," is asking about the carry-over limit, not a separate entitlement figure — the row's "Carry-over limit, days" field answers it directly. I did not find a separate document specifically about carrying leave into a new year; the row itself was sufficient and I did not need to open `annual-leave` or the other attendance-area tables that showed up in the overlay's working set.
