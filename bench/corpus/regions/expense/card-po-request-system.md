---
id: card-po-request-system
name: "Purchase order system defaults"
kind: system
one_liner: "What the PO system carries forward automatically, and why cumulative spend still needs a manual check"
parent: sec-card-or-purchase-order
---
# What the purchase order system fills in automatically

## What's automatic
Once a supplier's business registration number is entered once, the system carries forward their name, registration and payment terms on every later PO. The approval band also populates itself from the requester's level and the amount entered.

## What isn't automatic
**The system does not track cumulative monthly spend against a single supplier across separate PO requests.** Each request is checked against the quote and approval bands on its own amount — nobody's spend history rolls forward automatically, which is exactly what let a repeat purchase slip past the quote threshold in practice.

## What still needs a manual entry
- The quote reference and its date, checked by eye against the 60-day window
- Any note explaining a recurring supplier relationship, if one exists
- Confirmation that a supplier genuinely requires a PO rather than defaulting to one out of habit

Procurement's monthly reconciliation is where the cumulative check actually happens — the system only ever sees one request at a time.
