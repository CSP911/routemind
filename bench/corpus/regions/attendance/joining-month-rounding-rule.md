---
id: joining-month-rounding-rule
name: "Rounding a join date into a proration month"
kind: rule
one_liner: "How a join date that falls mid-month is rounded to the nearest month band before the joining-month table is applied"
parent: sec-mid-year-joiner-cases
---
# Rounding a join date into a proration month

The joining-month table assumes a clean month. A join date landing mid-month has to be rounded to one before the table can be read.

## The rounding bands

| Join date falls on | Counted as |
|---|---|
| 1st–15th of the month | That calendar month |
| 16th–last day of the month | The following calendar month |

An employee joining on 10 June is treated as a June joiner. An employee joining on 20 June is treated as a July joiner — losing June entirely from the proration count, not gaining a partial June.

## Why the boundary matters

The rounding happens once, at entry, and is not revisited. It is recorded alongside the service start date so payroll and the leave system read the same rounded month.

**A joiner assumes the actual calendar date is what accrues — it is the rounded month that accrues, not the date itself.** Someone starting on the 16th gets one fewer month of first-year accrual than someone starting on the 15th, two calendar days apart.

Once the month is set, the actual day count comes from the joining-month table, not from this rule.
