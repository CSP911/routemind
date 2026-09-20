---
id: cancellation-deadline-table
name: "Cancellation deadlines by leave status"
kind: table
one_liner: "How much notice cancelling a booked day needs, and what happens once it has already started"
parent: sec-booking-cases-1
---
# Cancellation deadlines by leave status

Cancelling a booked day restores the balance only if it happens within the right window, and the window depends on whether the leave has already started.

## Deadlines

| Leave status | Cancellation deadline | Balance outcome |
|---|---|---|
| Not yet started | Any time before the first day begins | Fully restored |
| Started, multi-day block | Before the next day begins | Remaining days restored |
| Already taken | Not applicable | Not restored |

## Why the line falls where it does

The attendance system checks the current date against the leave start date at the moment cancellation is filed, not the date the leave was originally approved.

**Cancelling a multi-day block partway through only restores the days still ahead — the day already in progress at the moment of cancellation is not refunded even if it is cancelled before that day ends.**

A worked walkthrough of both timings is covered separately in the leave-cancellation case; this table is the reference for the deadlines themselves.
