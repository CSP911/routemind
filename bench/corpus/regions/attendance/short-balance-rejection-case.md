---
id: short-balance-rejection-case
name: "A request rejected for short balance"
kind: case
one_liner: "A worked example of a multi-day leave request failing because the balance does not cover it"
parent: sec-booking-cases-2
---
# A request rejected for short balance

## The case
An employee with 2 days remaining requests three consecutive days off. The system rejects the request outright — it does not partially approve the two days that are covered and drop the third.

## Why it fails whole, not partial
Leave requests are evaluated as a single block. A 3-day request against a 2-day balance is a shortfall of 1 day, and the whole request is refused rather than reduced to fit.

## The trap
**A manager can still approve the request in the system before any balance check runs, giving the employee the impression it went through — the shortfall is only caught when payroll reconciles the leave ledger, sometimes days later, and the employee is then asked to either shorten the leave already taken or cover the extra day as unpaid leave.** Waiting for the automatic rejection at submission time avoids this entirely.

## What to do instead
Split the request: book the two covered days now, and submit the third day separately once more balance accrues, or after confirming with the HR desk whether unpaid leave applies.
