---
id: short-balance-half-day-case
name: "A half-day request against a fractional balance"
kind: case
one_liner: "A worked example of a half-day request being rejected because a quarter-day balance cannot cover it"
parent: sec-booking-cases-2
---
# A half-day request against a fractional balance

An employee has a quarter-day (0.25) balance remaining and requests a half-day (0.5) off the following week.

## What happens

| Item | Value |
|---|---|
| Balance remaining | 0.25 day |
| Requested | 0.5 day |
| Outcome | Rejected in full |

The system checks a fractional balance the same way it checks a full-day balance: the requested amount must be fully covered before approval, or the request does not go through at all.

**The request is not partially approved for the 0.25 day that is available — a shortfall of even a quarter day rejects the whole half-day request, the same outright rejection used for multi-day shortfalls.**

The employee's options are to request a quarter-day instead, or to wait for the next accrual date before booking the half-day.

This mirrors the treatment of a multi-day shortfall described in the short balance rejection case — the unit changes, the rejection rule does not.
