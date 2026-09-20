---
id: expense-close-system
name: "What the close system locks automatically"
kind: system
one_liner: "What the monthly close system locks on its own at the close date, and what still needs a manual entry before the batch can be marked closed"
parent: sec-month-end-close-and-expense-audit
---
# What the close system locks automatically, and what still needs a hand

## What locks at the close date
On the close date, the system freezes the claim queue. Every claim already submitted moves into that month's batch; anything not yet submitted rolls automatically into next month's. The system also auto-flags claims into the audit sample as they come in — any split payment at one merchant over 30,000 KRW, any disbursement form sitting near the roughly 100,000 KRW ceiling, and a random cut across the rest.

## What still needs a manual entry
The system does not chase a pending approval. If a team lead hasn't signed off a claim by the close date, the claim still locks into that month's batch as unapproved — the sign-off has to be added by hand afterward before the batch can be marked closed. It also doesn't answer a finding on its own: once the audit desk raises one, someone has to log the response before the record shows it resolved.

## The trap
**A claim still waiting on approval at the close date locks into that month's batch anyway — holding it back until the sign-off lands only pushes the whole claim into next month instead.** File it as soon as it's ready and let the approval follow.

Which claims the system pulls into the sample beyond this automatic flagging is a separate question, covered on its own.
