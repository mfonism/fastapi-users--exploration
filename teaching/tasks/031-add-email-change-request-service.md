# 031: Add Email-Change Request Service

## Task Metadata

| Field | Value |
|---|---|
| ID | 031 |
| Title | Add email-change request service |
| Parent epic | E6: Email-change workflow |
| Sibling tasks | 030, 032, 033 |
| Blocking tasks | 011, 030 |
| Blocked tasks | 032 |
| Time estimate | 60-75 minutes |
| Difficulty | Intermediate |
| Parallelizable | Yes, branch D |
| Suggested labels | `service-layer`, `email-change`, `validation` |
| Suggested commit | `feat: request email changes` |

## Rich Description

Implement the business rules for starting an email-change request. The service
normalizes the new email, rejects invalid changes, cancels unresolved older
requests, creates a new token, and returns the token for notification.

## Learning Goal

Students learn how services keep route handlers small and enforce multi-step
domain rules.

## Files Created Or Modified

- `src/explore/auth/email_changes/exceptions.py`
- `src/explore/auth/email_changes/service.py`

## Exact Implementation Objective

Create `request_email_change` and `cancel_unresolved_email_changes`.

## Acceptance Criteria

- New email is normalized.
- Same-email requests raise `EMAIL_CHANGE_SAME_EMAIL`.
- Already-used emails raise `EMAIL_CHANGE_EMAIL_TAKEN`.
- Existing unresolved requests for the same user are cancelled.
- New request stores old email, new email, token hash, and expiry.
- Service returns both the model object and raw token for notification.

## Teaching Notes

Point out that the route should not know how to cancel older requests. That is
business logic.

