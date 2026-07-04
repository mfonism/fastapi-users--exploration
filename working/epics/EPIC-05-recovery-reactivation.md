# EPIC-05: Recovery And Reactivation

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Status | Backlog |
| Priority | P1 |
| Milestone | Recovery |
| Labels | `backend`, `auth`, `security`, `recovery` |
| Child issues | EXP-014, EXP-015 |
| Blocking epics | EPIC-04 |
| Blocked epics | EPIC-07 |

## Objective

Support password recovery, authenticated password changes, and account
reactivation without leaking sensitive account existence or state.

## Success Criteria

- Forgot-password and reset-password flows work for eligible users.
- Authenticated users can change passwords after verifying the current password.
- Deactivated users can request and confirm reactivation.
- Stale, expired, reused, deleted-user, and invalid tokens are rejected.

## Notes For Junior Engineers

Recovery flows are security-sensitive. Start with tests for bad tokens and
edge cases before writing service logic.

