---
id: card-po-approver-role
name: "Purchase order approver"
kind: role
one_liner: "Which desk signs off a PO, banded by amount rather than by title alone"
parent: sec-card-or-purchase-order
---
# Who approves a purchase order

A purchase order follows the same approval ladder as the card, banded by amount rather than by title alone.

## Approval bands

| Requester level | PO approval limit | Above this |
|---|---|---|
| Staff | 300,000 KRW | Team lead approves |
| Team lead | 1,000,000 KRW | Division head approves |
| Division head and above | 3,000,000 KRW | Needs finance sign-off |

## Where this splits from card approval
The card's per-transaction cap decides what the card itself will authorise. The PO approval band decides who has to sign the request before it goes to the supplier. **A purchase that would clear easily on the card can still need a division head's signature on the PO**, if the supplier only accepts a PO and the amount sits above your own band.

## Escalation
If the request sits above your approval band, it doesn't wait — it routes automatically to the next level up rather than bouncing back to the requester.

Procurement holds the final PO number; the approver above only confirms the amount and the quote attached to it.
