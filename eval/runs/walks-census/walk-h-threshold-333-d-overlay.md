1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For category C4, amount V4, term M4, whose signature do I need, and do I have to get other prices first?" --member /v1/regions/procurement "approval threshold by category, amount and term is the procurement table's stated scope"
./bench/rmcli.py table /v1/nodes/sec-hard-threshold
./bench/rmcli.py read /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m4/body
./bench/rmcli.py overlay close --id ov_2026-09-21_ccaa50 --outcome answered --used /v1/nodes/sec-hard-threshold/body /v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m4/body

2. **Answer**:
For category C4, amount V4, term M4: the CFO must sign it off. Yes, other prices are required first — three competing quotes plus a written comparison. (Delegation limit for this row is 100,063 thousand KRW; expect 14 working days.)

3. **Source**:
/v1/nodes/sec-hard-threshold/body (table listing, confirmed this is the current threshold table, in force from 2026-01-01)
/v1/nodes/hard-threshold-row-category-c4-amount-v4-term-m4/body (the row itself, answer taken from here)

4. **Notes**:
The procurement table listing surfaced a loud warning that the approval-threshold document has THREE historical versions (`threshold-table`, `hard-threshold-v2`, and the current `sec-hard-threshold`), each superseded on a different date, plus a matching diligence-version warning for a different topic. That's the spot where it would be easy to grab a stale row by mistake. I avoided it because `sec-hard-threshold`'s own table header explicitly states "in force from 2026-01-01," which covers today's date (2026-09-21), and the row body itself repeats "In force from 2026-01-01" with a note on the prior versions — so I didn't need to separately open `hard-threshold-legend-revision` to be sure I had the current one, though I'd have opened it if the dates had been at all ambiguous.

The C4/V4/M4 codes in the question mapped directly onto an address the table printed (`hard-threshold-row-category-c4-amount-v4-term-m4`), so I never needed the amount/category/term legend files — no need to translate a plain-English description into a code here since the question was already given in coded form. That felt slightly too easy and worth flagging in case a future variant of this question gives a description ("a $50k marketing contract for 18 months") instead of pre-coded values, which would require reading the three legend files first.

One bookkeeping oddity: closing the overlay reported both addresses I used as "reached" rather than as named members — I had only added `/v1/regions/procurement` as a member and then browsed onward via `table`/`read` without a matching `overlay add`. The close still succeeded and recorded the outcome correctly, but the tool's language implies overlay membership and actual usage are tracked separately; worth keeping in mind not to assume "read" implies "added."
