---
id: leave-balance-check-timing
name: "When the balance check actually happens"
kind: rule
one_liner: "The point in the approval flow where an insufficient balance blocks a request, and where it doesn't"
parent: sec-booking-cases-1
---
# When the balance check actually happens

## Two different checks
The leave system checks balance sufficiency in two places, and they don't always agree at the moment of submission.

| Stage | Balance check |
|---|---|
| Employee submits request | Checked live — a request exceeding the current balance is rejected on the spot |
| Manager approves request | Not re-checked — approval can go through even if the balance has since dropped |
| Payroll reconciliation | Checked again at period close — any shortfall is flagged after the fact |

## The trap
**A request can be submitted and rejected for short balance, then resubmitted later once other leave is cancelled and the balance is restored, and approved without anyone re-checking whether the original shortfall reason still applies.** The system only ever compares against the balance at the instant of that specific check — it does not remember why an earlier attempt failed.

## Why this matters
Anyone chasing a rejected request should look at the balance at the moment of resubmission, not at whatever the balance was during the earlier failed attempt.

This is the same gap that lets a manager-approved request later fail at payroll, as in the short-balance case.
