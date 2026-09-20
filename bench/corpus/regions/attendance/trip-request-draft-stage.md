---
id: trip-request-draft-stage
name: "The draft trip request"
kind: rule
one_liner: "How long a trip request can sit unsubmitted before it disappears"
parent: sec-trip-approval-before-the-trip
---
# The draft trip request

Opening the trip request form and entering dates does not submit anything. It creates a draft, visible only to the employee, that has to be submitted before any approval clock starts.

## What a draft holds
A draft can be edited freely — dates, destination, purpose — with no notice requirement, because nothing has been sent to an approver yet. It is not attendance data and does not appear on any manager's queue.

## The 7-day expiry
A draft that is never submitted is deleted automatically 7 days after it was created. **This is a hard deletion, not an archive** — the dates, destination and any notes entered are gone, and recreating the request means starting over, including recalculating whether the lead time in the approval deadline table still works for the intended departure date.

## After submission
Once a draft is submitted it stops being a draft. Further changes — a different date, an added leg — go through an amendment to the pending request, not a new draft, and can restart the approval clock depending on what changed.

The lead time that clock has to clear before departure is set out separately by trip type.
