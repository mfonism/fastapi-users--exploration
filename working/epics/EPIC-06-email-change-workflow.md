# EPIC-06: Email Change Workflow

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Status | Backlog |
| Priority | P2 |
| Milestone | Email Change |
| Labels | `backend`, `auth`, `email-change`, `security` |
| Child issues | EXP-016, EXP-017 |
| Blocking epics | EPIC-04 |
| Blocked epics | EPIC-07 |

## Objective

Allow verified users to request and confirm email address changes using hashed
tokens, expiry, cancellation, and session invalidation.

## Success Criteria

- Email-change requests are stored in a dedicated table.
- Raw confirmation tokens are never stored.
- Existing unresolved requests are cancelled when a new one is created.
- Confirmation updates the user's email and verification timestamp.
- Matching current sessions are logged out.

## Notes For Junior Engineers

This is the most complex workflow. Split your thinking into request creation,
token lookup, usability checks, user checks, email update, and session logout.

