---
id: public-holiday-leave-booking-table
name: "How many days to book across a public holiday"
kind: table
one_liner: "How many calendar days a leave block spans versus how many are actually deducted when a public holiday falls inside it"
parent: sec-booking-cases-2
---
# How many days to book across a public holiday

## The table
| Leave block | Calendar days booked | Days deducted from balance |
|---|---|---|
| Mon–Fri, one public holiday mid-week | 5 | 4 |
| Mon–Fri, no public holiday | 5 | 5 |
| Single day that is itself a public holiday | 1 | 0 — no booking needed |

## The trap
**Booking the public holiday itself as a leave day, instead of leaving it out, does not double-charge the balance — the system still deducts nothing for that day — but it leaves a leave record sitting on a day that never needed one**, which shows up as an anomaly when HR reconciles the year-end balance.

## What still needs a separate booking
Only holidays that fall inside a leave block booked as one continuous request are skipped automatically. A holiday with no leave request touching it needs no booking at all, and a holiday immediately before or after a block does not extend that block on its own — see public holiday floating days for which holidays qualify for the automatic skip.
