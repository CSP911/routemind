1. **Commands**

```
./bench/rmcli.py table
./bench/rmcli.py overlay create --question "In January 2024, how much leave was accrued or granted for someone with two years of continuous service? Answer under the version of leave accrual that was in force on that date." --member /v1/regions/attendance "leave accrual by tenure/service years is covered under attendance"
./bench/rmcli.py read /v1/nodes/hard-accrual-legend-revision/body
./bench/rmcli.py table /v1/regions/attendance
./bench/rmcli.py table /v1/nodes/annual-leave
./bench/rmcli.py overlay add --id ov_2026-09-20_7d139c --address /v1/nodes/leave-accrual --why "legend says version in force until 2024-07-01 lives here, indexed by one qualifier — this is the version for Jan 2024"
./bench/rmcli.py read /v1/nodes/accrual-rule/body
./bench/rmcli.py overlay close --id ov_2026-09-20_7d139c --outcome answered --used /v1/nodes/hard-accrual-legend-revision/body /v1/nodes/accrual-rule/body
```

2. **Answer**

15 days. Under the leave accrual rule in force until 2024-07-01, someone with 2 years of continuous service falls in the "1 year and over" bracket (the next bracket, "3 years and over", doesn't apply yet), which grants 15 days, unchanged from the 1-year rate — the +1-every-2-years escalation only starts at the 3-year mark.

3. **Source**

- `/v1/nodes/hard-accrual-legend-revision/body` — establishes that leave accrual has three versions by date, and that the pre-2024-07-01 version (at `leave-accrual`) is the one that answers a January 2024 question.
- `/v1/nodes/accrual-rule/body` — the actual entitlement table for that version, giving the "1 year and over: 15 days" figure used.

4. **Notes**

- The trap here is real: the overlay seeded from the attendance table surfaces `hard-accrual-v2` (2024-07-01 to 2025-12-31) and `sec-hard-accrual` (current, since 2026-01-01) directly, but the oldest version — the one actually in force in January 2024 — isn't listed at that level at all, and the legend page explicitly warns that "the oldest says nothing at all about having been replaced." Grabbing `hard-accrual-v2` because its date range looks closest, or asking for the accrual table by name and taking whatever comes back "current," would both give the wrong answer.
- The oldest version's address (`/v1/nodes/leave-accrual`) only turns up one hop further, under `/v1/nodes/annual-leave` — it isn't a sibling of the other two version files in the attendance table listing, so a walk that stops at the attendance table's own rows would miss it.
- Also worth flagging: this old version's table has coarser brackets than the newer ones (just "1 year and over" and "3 years and over," no explicit "2 years" row), so the two-year case has to be read off the "1 year and over" bracket rather than finding a bracket that names two years directly.
