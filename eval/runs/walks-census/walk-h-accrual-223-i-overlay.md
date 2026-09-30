1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py overlay create --question "3 days/week, 5 years tenure, fully remote: monthly leave accrual rate and max carryover balance allowed in January" --member /v1/nodes/sec-hard-accrual "current leave accrual table by type, tenure, site" --member /v1/nodes/annual-leave "entitlement and carryover/booking rules"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-type/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-tenure/body
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-site/body
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_3d7cc3 --outcome answered --used /v1/nodes/hard-accrual-legend-type/body /v1/nodes/hard-accrual-legend-tenure/body /v1/nodes/hard-accrual-legend-site/body /v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l4/body

2. **Answer**
Accrues 1.26 days per month. Carry-over limit (the most that can still be held going into January) is 13 days. This is under the current accrual table, in force since 2026-01-01. (Also noted: accrual stops during unpaid leave, and 4 working days' notice is required to book leave — not asked for but on the same row.)

3. **Source**
/v1/nodes/hard-accrual-legend-type/body (mapped "three days a week" → type E3)
/v1/nodes/hard-accrual-legend-tenure/body (mapped "been here five years" → tenure T3)
/v1/nodes/hard-accrual-legend-site/body (mapped "fully from home" → site L4)
/v1/nodes/hard-accrual-row-type-e3-tenure-t3-site-l4/body (the figures: 1.26 days/month accrual, 13-day carry-over limit)

4. **Notes**
The three qualifiers in the question ("three days a week", "five years", "fully from home") map directly and unambiguously onto the three legend tables (type/tenure/site) — no guessing needed, each phrase matched a legend row's wording closely. The only mild friction: the overlay's two members were the section-level tables (sec-hard-accrual, annual-leave), not the individual row/legend files — so I had to open sec-hard-accrual's children directly rather than finding them pre-listed as overlay members, and the overlay `close` command reported the four addresses I actually used as "reached" (i.e. answered from somewhere the overlay never explicitly named as a member) rather than a plain match. Not a real problem, just worth flagging since it could look like an error. Also worth flagging: there are three versions of the accrual table (a "legend-revision" file warns of this); I used the current one (sec-hard-accrual, in force since 2026-01-01), which is correct since "today" is 2026-09-20/21, but this is an easy place to grab a superseded row (hard-accrual-v2) by mistake if the /v1/nodes/hard-accrual-legend-revision warning is skipped.
