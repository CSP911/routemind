---
id: prepaid-card-virtual-number-expiry
name: "How long a single-use virtual number stays open"
kind: deadline
one_liner: "The window a virtual number stays valid before it lapses unused, and why generating one too early backfires"
parent: sec-prepaid-and-virtual-cards
---
# How long a single-use virtual number stays open

A single-use virtual number generated for an online purchase isn't permanent — it's built to cover one transaction within a set window, then it closes itself whether or not it was used.

## The window
- A virtual number is valid for **24 hours** from generation if unused
- Once the transaction posts, the number closes immediately — it can't be reused even inside that window
- An unused, expired number doesn't need to be reported; it simply drops off the list finance reconciles against

## The trap
**Generating a number ahead of a purchase you're not ready to make yet — say, waiting on a manager's go-ahead — often means it's expired by the time you actually check out**, and the fix is a fresh number, not retrying the same one after the 24 hours pass.

## Extending it
There's no extension request for a single-use number. If the purchase is delayed past 24 hours, request a new number through the same portal; the old one simply lapses.

This is different from a standing prepaid card's balance, which doesn't expire on a clock at all — it sits until someone reports it or its reconciliation date passes.
