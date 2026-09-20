---
id: claim-system-of-record
name: "Where the trip record actually lives"
kind: system
one_liner: "The attendance system holds the trip dates and status, the claim system only references them"
parent: sec-the-handover-to-a-claim
---
# Where the trip record actually lives

The attendance system and the claim system are separate pieces of groupware, and only one of them can change a trip's dates or status.

## Attendance system

Holds the trip request, its confirmed status, and the dates as approved and adjusted by the line manager. This is the system of record for anything about whether and when the trip happened.

## Claim system

Holds the daily allowance claim itself — the form, the bank details, and the payment status. It reads the trip's dates from the attendance system at the moment the claim is filed; it does not keep an independent copy that can drift on its own.

**Editing a date inside the claim system does not change the underlying attendance record — it only creates a fresh mismatch, because the claim system reads from attendance, not the other way round.**

Once the allowance claim clears, the same trip becomes eligible for the broader expense settlement handoff.
