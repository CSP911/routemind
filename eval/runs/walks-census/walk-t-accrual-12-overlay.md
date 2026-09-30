1. **Commands**
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "Which two versions of leave accrual docs are needed to reconcile 2023 and 2025 claims, and how much leave was accrued/granted under each?" --member /v1/regions/attendance "leave accrual policy versions likely live here"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/sec-hard-accrual
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py overlay add --id ov_2026-09-20_aca29e --address /v1/nodes/leave-accrual --why "oldest accrual version, in force until 2024-07-01, needed for 2023 claims"
./bench/rmcli.py overlay remove --id ov_2026-09-20_aca29e --address /v1/nodes/attendance-system --why "not relevant, groupware menus not policy figures"  [failed: 404, not a direct overlay member]
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py overlay close --id ov_2026-09-20_aca29e --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/accrual-rule/body /v1/nodes/hard-accrual-v2/body

2. **Answer**
Leave accrual has three documented versions; a 2023 claim and a 2025 claim each fall under a different one (neither is the current, 2026-01-01-onward table).

- **For 2023 claims** — the oldest version, "Leave entitlement" (in force until 2024-07-01), indexed by service length only:
  - Under 1 year: 1 day per completed month (up to 11 days)
  - 1 year and over: 15 days
  - 3 years and over: 15 days, +1 every 2 years (capped at 25)
  - Granted on a fiscal-year basis (1 Jan–31 Dec); unused days do not carry over and lapse balances are paid out.

- **For 2025 claims** — the second version, "Leave accrual, 2024-07-01 to 2025-12-31" (indexed by type and tenure), monthly accrual rate:
  | type \ tenure | T1 | T2 | T3 | T4 |
  |---|---|---|---|---|
  | E1 | 0.40 | 0.42 | 0.44 | 0.46 |
  | E2 | 0.48 | 0.50 | 0.52 | 0.54 |
  | E3 | 0.56 | 0.58 | 0.60 | 0.62 |
  | E4 | 0.64 | 0.66 | 0.68 | 0.70 |
  (Carry-over limit and notice-required figures were unchanged from the oldest version in this window.)

3. **Source**
- /v1/nodes/hard-accrual-legend-revision/body (identifies which of the three versions covers which date range)
- /v1/nodes/accrual-rule/body (the 2023 figures — oldest version, "Leave entitlement")
- /v1/nodes/hard-accrual-v2/body (the 2025 figures — second version, 2024-07-01 to 2025-12-31)

4. **Notes**
- The overlay's first hop off /v1/regions/attendance never surfaced the oldest version's actual document — it listed `sec-hard-accrual` (current, 2026-01-01 onward) and `hard-accrual-v2` (2024-07-01–2025-12-31) directly, but the oldest one only showed up once I opened `annual-leave` → `leave-accrual` → `accrual-rule/body`. Reaching for "the leave accrual doc" from the region table alone would have missed the 2023 answer entirely.
- The legend-revision doc explicitly warns that "the oldest says nothing at all about having been replaced" and that reaching for the newest is wrong for anything before 2026-01-01 — without reading it first I'd have been tempted to answer 2025 from `sec-hard-accrual` (current table) since it was the most prominent, larger, more detailed table in the listing. That would have been wrong: 2025 is fully inside the *second* version's window (2024-07-01 to 2025-12-31), not the current one.
- A `remove` on `/v1/regions/attendance`'s child `attendance-system` failed with 404 ("not in this overlay") — sub-rows shown under a table member aren't themselves addressable overlay members unless explicitly `add`ed, only the table address itself was. Harmless, but worth noting as a rough edge.
- The final `overlay close` marked the two content documents as "reached... from somewhere the overlay never named" — I'd added the parent table (`/v1/nodes/leave-accrual`) as a member but read the deeper `/body` files directly rather than adding those exact file addresses to the overlay first. Didn't affect the answer, just a bookkeeping nuance in how the overlay tracks "used" vs. "member" addresses.
