---
id: expense-subscription-registry-system
name: "What the subscription registry tracks automatically"
kind: system
one_liner: "What the registry auto-populates from the card feed, and what still needs a manual entry"
parent: sec-subscription-lifecycle
---
# What the subscription registry tracks automatically

The registry pulls recurring charges directly from the corporate card feed, but it can only reconcile a figure against a field that was filled in at registration.

## Auto-populated
- Charge amount and date, from the card feed
- Vendor name, matched against the merchant string on the statement
- Running total for the fiscal year, per vendor

## Still manual
- Seat count, since the card feed has no visibility into how many people use a licence
- Budget owner and cost centre
- Renewal notice deadline, unless the vendor's terms were entered at registration

**A charge that renews under a slightly different merchant string than the one on file doesn't match to the existing entry — it creates a second, unlinked line instead**, which is how one subscription ends up looking like two.

Where the registry falls short, the quarterly seat audit and the ownership handover are what catch what it leaves behind.
