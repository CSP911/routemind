---
id: evidence-reissue-system
name: "How pending reissues are tracked"
kind: system
one_liner: "What the pending-reissue queue does while a statement of circumstances is waiting, and what happens if the window closes"
parent: sec-evidence-in-awkward-cases-2
---
# How pending reissues are tracked

## The queue
Once a statement of circumstances is filed against a missing e-receipt, the claim line moves into a pending-reissue state rather than being rejected outright. It stays there while the merchant is given the standard 3–5 working days to resend the original.

## What happens at the deadline
If the reissue arrives inside the window, it replaces the statement and the claim clears normally. If it doesn't, the system does not keep waiting indefinitely.

## The trap
**A claim left in pending-reissue past the window is not quietly extended — it is auto-flagged for the 2% penalty at the next settlement run**, whether or not anyone remembers to chase the merchant again. Getting the document a week later does not undo that; the penalty applies at settlement, not at whenever the paperwork eventually shows up.

Chasing the merchant directly, rather than waiting on the queue, is almost always faster than the fallback route.
