---
id: prepaid-card-lost-virtual-number-case
name: "A charge that landed after the number should have expired"
kind: case
one_liner: "A worked case where a queued checkout cleared past a virtual number's window and produced a duplicate charge"
parent: sec-prepaid-and-virtual-cards
---
# A charge that landed after the number should have expired

A finance officer flagged a 45,000 KRW charge against a virtual number that had shown as expired on the portal two days earlier. The holder had generated the number for a one-off software licence, the vendor's checkout timed out, and the holder assumed the purchase had failed outright.

## What actually happened
The vendor's checkout had queued the payment rather than failing it, and processed it 36 hours later — past the number's 24-hour window, but the bank's authorisation had already been reserved before the timeout, so the charge cleared on the original number regardless of what the portal showed.

## Why it wasn't caught sooner
The holder generated a second number for the same purchase, assuming the first had failed cleanly, and the vendor didn't refund the duplicate on its own — it fulfilled two licences instead of one.

## The trap
**A queued or "processing" checkout is not a failed one — generating a second virtual number before confirming the first attempt was actually declined can produce two charges for one purchase**, and the vendor has no obligation to reverse the second unasked.

## Resolution
The duplicate licence was cancelled with the vendor directly, and the refund followed the standard partial-refund reporting line once it landed on the account.
