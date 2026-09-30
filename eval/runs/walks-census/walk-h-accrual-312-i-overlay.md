1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Partner firm employee, 2 years tenure, Singapore entity: monthly leave accrual rate and January carry-forward cap" --member /v1/regions/attendance "leave accrual, carry-forward and cap rules are covered here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l3/body
./bench/rmcli.py overlay close --id ov_2026-09-20_fe15e7 --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/sec-hard-accrual /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l3/body

2. **Answer**
Accrues 1.48 days of leave per month. Carry-over limit is 9 days — that is the most that can still be held into January.

3. **Source**
/v1/nodes/hard-accrual-legend-revision/body
/v1/nodes/sec-hard-accrual
/v1/nodes/hard-accrual-legend-type/body
/v1/nodes/hard-accrual-legend-tenure/body
/v1/nodes/hard-accrual-legend-site/body
/v1/nodes/hard-accrual-row-type-e4-tenure-t2-site-l3/body

4. **Notes**
The biggest trap here was the three-version accrual history: `leave-accrual` (until 2024-07-01), `hard-accrual-v2` (2024-07-01 to 2025-12-31), and `sec-hard-accrual` (2026-01-01 onwards, "the current table"). Since today's date is 2026-09-20/21, the current table is correct, but the legend-revision page's own warning — "reaching for the newest is wrong for anything before 2026-01-01" — made me stop and confirm the date qualified before trusting the "current" label instead of just grabbing the newest-looking node by name.
The three qualifiers (type/tenure/site) are opaque codes (E1–E4, T1–T4, L1–L4) with no meaning stated on the row table itself — each had its own legend file, and the mapping from the question's plain-English phrasing to a code was not obvious until read. "Here from our partner firm" maps to type E4 specifically (distinct from "on a two-year contract" = E2, which "two years" in the question could have been mistakenly matched to if I'd conflated tenure wording with employment-type wording — the question's "been here two years" is tenure T2, not employment type). That was the closest near-miss: two different phrases in the question both contain "two years," and they map to different axes (employment type vs. tenure), so care was needed not to double-count "two years" onto the wrong legend.
"How much can I still be holding in January" was interpreted as the carry-over limit (9 days), since that is the only figure on the row governing how much accrued leave persists past year-end.
