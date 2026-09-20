---
id: expense-subscription-vendor-price-change-case
name: "A vendor price change landing mid-cycle"
kind: case
one_liner: "A worked case where a licence renewed at a higher tier than the budget line assumed"
parent: sec-subscription-lifecycle
---
# A vendor price change landing mid-cycle

## The starting position
A 15-seat team licence was registered the previous year at 10,000 KRW per seat, sitting inside the 11–25 seat tier. The following year's budget line was set at that same rate, times 15 seats, with no adjustment expected.

## What changed
The vendor restructured its pricing three months before renewal, folding the 11–25 tier into a new band starting at 11,000 KRW per seat. No seat count changed on the team's side — the licence renewed automatically at the new rate.

## What it cost
The renewal charge landed 15,000 KRW higher than the budget line assumed, purely from the rate change, with the seat count unchanged throughout.

**Nothing here was a registration error or a seat drift — the mismatch was a vendor price change nobody had a step to catch, because the registry only tracks seat count and renewal date, not the per-seat rate itself.** The fix going forward is to check the vendor's current rate card before each renewal, not just the seat count, and log any rate change as its own line rather than folding it into the existing forecast silently.

This is the kind of gap the monthly budget variance report is built to surface, once the charge has already landed.
