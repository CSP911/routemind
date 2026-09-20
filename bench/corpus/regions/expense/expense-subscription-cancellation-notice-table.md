---
id: expense-subscription-cancellation-notice-table
name: "Cancellation notice by billing cycle"
kind: table
one_liner: "How far ahead a cancellation has to be filed before auto-renew locks in, by billing cycle"
parent: sec-subscription-lifecycle
---
# Cancellation notice by billing cycle

Not every subscription gives the same warning before it renews. The vendor sets the actual notice period, but the registry tracks a deadline against each entry so nobody has to remember the vendor's terms from memory.

| Billing cycle | Typical notice required | Where it's tracked |
|---|---|---|
| Monthly | At least 3 business days before the billing date | Registry entry, auto-flagged |
| Annual | Per the licence's stated non-renewal window | Registry entry, flagged 60 days ahead |
| Multi-year | Per contract terms, often 90 days or more | Registry entry, flagged at contract start |

**The registry's flag is a reminder, not the deadline itself** — if the vendor's real notice window is longer than what was entered at registration, the charge still renews on the vendor's terms, not the registry's.

Filing inside the window stops the next charge; filing after it does not reverse a charge already committed, which is the same rule that governs a renewal that lands on the card unexpectedly.
