## Commands
./bench/rmcli.py table
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py table /v1/nodes/leave-accrual
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py read /v1/nodes/hard-accrual-v2/body

## Answer
Two versions are needed:

1. **For the 2023 claim** — the oldest version (in force until 2024-07-01), at `/v1/nodes/accrual-rule/body`:
   - Under 1 year: 1 day per completed month (up to 11)
   - 1 year and over: 15 days
   - 3 years and over: 15 days, +1 every 2 years (capped at 25)
   - Granted on a fiscal-year basis (1 Jan–31 Dec); days granted 1 January, first-year accrual is monthly from joining date; unused days lapse 31 Dec and are paid out (no carry-over).

2. **For the 2025 claim** — the second version, in force 2024-07-01 to 2025-12-31, at `/v1/nodes/hard-accrual-v2/body`:
   - Monthly accrual rate by type × tenure:
     - E1: T1 0.40, T2 0.42, T3 0.44, T4 0.46
     - E2: T1 0.48, T2 0.50, T3 0.52, T4 0.54
     - E3: T1 0.56, T2 0.58, T3 0.60, T4 0.62
     - E4: T1 0.64, T2 0.66, T3 0.68, T4 0.70
   - All other terms (carry-over limit, notice required) followed the leave entitlement rule unchanged until 2026-01-01.

## Source
- /v1/nodes/hard-accrual-legend-revision/body (identifies which version covers which date range)
- /v1/nodes/accrual-rule/body (2023 claim — pre-2024-07-01 version)
- /v1/nodes/hard-accrual-v2/body (2025 claim — 2024-07-01 to 2025-12-31 version)

## Notes
The attendance table's listing was misleading at first glance: it shows `hard-accrual-v2` (superseded) and `sec-hard-accrual` (current, from 2026-01-01) side by side, with no oldest-version node visible at that level. It would be easy to conclude only two versions exist and to wrongly pick the current (2026) table for the 2025 claim, since 2025 is "recent." The legend-revision file explicitly warns against this: it states there are *three* versions, that "for a question dated in 2025 the answer is the middle one, not the oldest and not the current table," and that the oldest version "says nothing at all about having been replaced" — so nothing in that oldest document itself would tip you off that it had been superseded. The oldest version's actual address (`/v1/nodes/leave-accrual` → `/v1/nodes/accrual-rule/body`) isn't in the attendance-area table at all; it only surfaces by drilling into `/v1/nodes/annual-leave`, which is easy to skip if you assume "accrual" only lives under the `hard-accrual*` naming pattern.
