---
id: leave-cancellation-case
name: "Cancelling a booked day"
kind: case
one_liner: "A worked example of cancelling leave before and after it starts, and when the balance is restored"
parent: sec-booking-cases-1
---
# Cancelling a booked day

## The case
An employee books 27 August as a full day off. On 25 August they cancel it through the same leave menu. The system restores the 1.0 day to their balance immediately, as if the day had never been taken.

## Where the line falls
Cancellation before the leave day begins simply reverses the booking. **Cancelling on the morning of 27 August after the leave has already started does not reverse it — the day is already marked as taken and the balance is not restored.** An employee who calls in to cancel at 10am on the day itself, having already been recorded as on leave, needs a correction request rather than a simple cancellation.

## Practical effect
| Timing of cancellation | Outcome |
|---|---|
| Before the leave day starts | Balance restored, no trace left |
| After the leave day has started | Treated as leave taken; requires a correction request |

Same-morning cancellation is the mirror image of same-morning booking, covered separately.
