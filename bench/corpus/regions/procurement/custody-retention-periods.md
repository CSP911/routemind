---
id: custody-retention-periods
name: "Retention periods by contract status"
kind: table
one_liner: "How long an original stays in custody depending on whether it's active, ended, or under audit hold"
parent: sec-contract-custody-cases
---
# Retention periods by contract status

| Status | Retention period | Note |
|---|---|---|
| Active | For the life of the contract | Held in GA custody; borrowing requires the checkout log |
| Ended (expiry or fulfilment) | 5 years from end date | Runs from when the contract ended, not when it was signed |
| Terminated for cause | 5 years from termination date | Same window, different starting event |
| Under audit hold | Suspended | Clock pauses on any underlying period until the hold is lifted |

## The trap

**The 5-year window is measured from the end date, not the signing date.** A three-year contract that ran its full term is kept for 5 years after it ended — 8 years after it was signed — not 5 years after signing. Confusing the two dates is the most common reason a file gets destroyed early.

Electronically signed contracts run against the same table, measured from the same events.
