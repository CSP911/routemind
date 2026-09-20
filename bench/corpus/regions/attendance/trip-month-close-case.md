---
id: trip-month-close-case
name: "A trip spanning the month close"
kind: case
one_liner: "A worked example of which payslip a trip's days land on when the trip crosses a payroll cutoff"
parent: sec-trip-attendance-cases
---
# A trip spanning the month close

An employee's trip runs from the 28th of one month through the 3rd of the next, with the payroll cutoff falling on the 25th.

## Which payslip each day hits

| Trip days | Payroll month |
|---|---|
| 28th–30th/31st | Current month's payslip |
| 1st–3rd | Next month's payslip |

Both halves of the same continuous trip are still entered as ordinary trip days — the split only affects which payslip picks them up, not how the days are classified.

**The trap is treating the trip as one block and entering it all against a single month because it was booked as a single request — the system reads by day against the cutoff, not by request.** A trip request that straddles the cutoff without both halves confirmed in the system will show correctly on one payslip and be missing entirely from the other.

This is the same cutoff logic used when a cancelled leave day's correction has to carry into the following month.
