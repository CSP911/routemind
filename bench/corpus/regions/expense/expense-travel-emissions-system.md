---
id: expense-travel-emissions-system
name: "What the emissions entry auto-fills"
kind: system
one_liner: "What the trip claim system carries over from an approved itinerary, and where a manual entry is still needed"
parent: sec-travel-emissions-reporting
---
# What the emissions entry auto-fills

The trip claim system reads an approved itinerary and populates mode and distance for each leg without anyone typing them in — for a straightforward single-mode trip, the emissions entry needs no manual work at all.

## What it gets right on its own
- Mode, taken from the booked ticket type
- Distance, taken from the city pair on the approved itinerary
- The correct factor applied automatically from the rate table

## Where it needs a manual entry
- A mid-trip itinerary change does not recalculate the emissions line on its own — the traveller has to re-enter the new leg
- A mixed-mode leg — rail for part of the distance, a personal car for the rest — populates only the first mode booked; the second has to be added by hand
- **A rebooked flight that replaces a cancelled rail ticket keeps the original rail entry unless someone deletes it** — the system has no way to know a ticket it never booked was cancelled

## Where this matters
Because the annual figure locks each January, an unflagged mid-trip change from earlier in the year can sit wrong for months before anyone notices it during a review.
