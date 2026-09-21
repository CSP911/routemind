1. **Commands**:
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "For type E2, tenure T3, site L4, how much time off am I building up each month, and how much can I still be holding in January?" --member /v1/regions/attendance "leave accrual rate and carryover/cap questions live in attendance"
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l4/body
./bench/rmcli.py overlay close --id ov_2026-09-20_bb56ad --outcome answered --used /v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l4/body

2. **Answer**:
For type E2, tenure T3, site L4 (current table, in force from 2026-01-01):
- Accrues 0.94 days per month.
- Carry-over limit: 13 days — this is the most you can still be holding once the year turns over into January.

3. **Source**:
/v1/nodes/hard-accrual-row-type-e2-tenure-t3-site-l4/body

4. **Notes**:
The table `/v1/nodes/sec-hard-accrual` is indexed directly by type/tenure/site code, so with all three qualifiers given in the question (E2, T3, L4) there was an exact-match row and no need to consult the legend files (hard-accrual-legend-type/tenure/site) that translate plain-language descriptions into these codes — those would matter if the question had described the person instead of naming the codes.

There are three versions of the accrual rules (`leave-accrual`, `hard-accrual-v2` superseded 2024-07-01 to 2025-12-31, and the current `sec-hard-accrual` in force from 2026-01-01). Today being 2026-09-20/21, the current table is the right one; it would be easy to grab the superseded v2 table by mistake if not reading the "in force" dates carefully — the row body itself flags this with an explicit note pointing to `hard-accrual-legend-revision` for the version history.

The question's "how much can I still be holding in January" phrasing initially read ambiguously — it could mean a monthly accrual amount for the month of January specifically, or the year-end carry-over cap that applies going into January. The row only has one figure that fits a "how much can I hold" framing — "Carry-over limit, days: 13" — so I took that as the answer; there is no January-specific accrual figure, since accrual is a flat 0.94/month with no month-by-month variation shown.

The overlay tool flagged the final `read` as "reached" — answered from an address never added as an overlay member. I drilled into `/v1/nodes/sec-hard-accrual`'s table listing and read the row body directly rather than first issuing `overlay add` for it. The answer is correct, but for a stricter walk the row address should have been added to the working set before reading it.
