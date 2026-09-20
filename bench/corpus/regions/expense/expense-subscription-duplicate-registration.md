---
id: expense-subscription-duplicate-registration
name: "Duplicate subscription registration"
kind: rule
one_liner: "Why the same recurring service can't be registered a second time under a different owner"
parent: sec-subscription-lifecycle
---
# Duplicate subscription registration

Two teams occasionally register the same vendor separately — one under a project code, one under a department budget — because neither checked whether the service was already on the card.

## The rule
- Before registering a new recurring service, check the registry for the vendor name. A duplicate entry is rejected at approval, not merged automatically afterward.
- If two teams genuinely need separate licences from the same vendor, both are registered under the same vendor entry with separate seat counts, not as two independent subscriptions.

**A duplicate registration that slips through renews as two full charges, not one shared one** — finance does not net them against each other later, since by then both have already been treated as legitimate ongoing spend.

Checking the registry first is quicker than untangling two live subscriptions afterward, and it's the same registry the seat audit and the ownership handover both draw from.
