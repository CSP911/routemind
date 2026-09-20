---
id: expense-subscription-seat-count-audit
name: "Seat count audit procedure"
kind: procedure
one_liner: "The steps to reconcile a team licence's billed seat count against who's actually using it"
parent: sec-subscription-lifecycle
---
# Seat count audit procedure

A per-seat subscription bills against whatever count was last confirmed, not the number of people currently logged in. Left unchecked, a team that shrinks keeps paying for seats nobody occupies.

## Steps
1. The budget owner pulls the vendor's active-user list each quarter.
2. Compare it against the seat count on the registry entry.
3. If the two don't match, file a seat adjustment with the vendor and update the registry in the same step — doing one without the other is exactly what lets the drift reappear next quarter.
4. Confirm the next invoice reflects the new count before closing the audit.

**A seat removed from the vendor's console without a formal adjustment request still bills** — most platforms treat "unused" and "unlicensed" as different things, and only the second one stops the charge.

Quarterly is the floor, not the ceiling — a team with frequent turnover should audit monthly instead. Drift that's gone unadjusted for longer than a quarter is handled as the worked case that follows.
