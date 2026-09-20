---
id: post-close-correction-table
name: "Post-close correction payroll timing"
kind: table
one_liner: "Which payslip a corrected attendance record reaches depending on when it is filed"
parent: sec-attendance-corrections-and-disputes
---
# Post-close correction payroll timing

| Correction filed | Payslip affected |
|---|---|
| Before month close | Same month, standard processing |
| Within 10 days after close | Same month, adjusted run |
| After the 10-day window (override approved) | Following month only |
| Disputed record still under escalation | Held until resolved, then next available run |

The "adjusted run" row is not automatic — payroll only reprocesses a closed month if the correction is filed inside the 10-day window from the correction deadline rule. Everything after that is next month, regardless of how obviously the record was wrong.

**A correction approved on paper before the 10-day deadline but entered into the system after it still counts as late — the system timestamp is what payroll reads, not the approval date.** Get the entry made, not just signed off, before the window closes.

How that approval actually gets recorded is covered next.
