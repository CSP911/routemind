---
id: expense-trip-days-system
name: "What the trip claim system auto-populates for allowance days"
kind: system
one_liner: "What the trip-days field fills in automatically from an approved itinerary, and where a late confirmation or month boundary needs a manual entry instead"
parent: sec-trip-days-versus-allowance-days
---
# What the trip claim system auto-populates for allowance days

## What populates on its own
Once a trip is approved before departure, the system reads the approved start and end dates and generates one allowance-day line for each calendar day in between, including weekends. It also tags any weekend day inside that range as a travel day rather than a working day, so it draws the daily allowance without triggering a second payment.

## What needs a manual entry
- **A trip confirmed after departure never gets this automatic run.** Approval that lands once the traveller is already on the road does not retroactively populate the allowance days — someone has to add each day by hand once the trip is closed.
- A trip crossing a month boundary is split into two lines automatically, one per calendar month, using the date rather than the trip's start date. No manual splitting is needed, but the two lines can land in different close cycles.
- A day the traveller was actually at a client site but the itinerary never listed stays invisible until someone adds it by hand — the system only knows what the approved itinerary told it.

Confirm before departure whenever a date is still possible; a same-day approval saves the manual clean-up later.
