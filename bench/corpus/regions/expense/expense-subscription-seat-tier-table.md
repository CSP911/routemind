---
id: expense-subscription-seat-tier-table
name: "Seat-count pricing tiers for team licences"
kind: table
one_liner: "The per-seat price bands a team licence renews into as headcount crosses a threshold"
parent: sec-subscription-lifecycle
---
# Seat-count pricing tiers for team licences

Most team subscriptions price per seat, and the per-seat rate drops as the seat count rises. The tier that applies is set at renewal, not the moment headcount changes.

| Seat count | Rate per seat per month |
|---|---|
| 1–10 seats | 12,000 KRW |
| 11–25 seats | 10,000 KRW |
| 26 and above | 8,000 KRW |

## Why the timing matters
Crossing from 10 seats to 11 partway through a billing cycle doesn't retroactively drop the rate on the current invoice, and dropping from 26 seats to 25 doesn't raise it either. Both take effect only at the next renewal.

**A team that trims seats mid-cycle to save money sees no change on the current charge, and finance flags the mismatch as if the reduction never happened — because it hasn't happened yet, pricing-wise.** The correct move is to record the seat change immediately in the registry and let the tier catch up at renewal, rather than assuming the saving starts the day the seat was removed.

This is the number the seat-count audit checks against — a tier applied a cycle late is the most common finding on that audit.
