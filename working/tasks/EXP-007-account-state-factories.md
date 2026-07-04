# EXP-007: Add User Account-State Behavior And Factories

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Story |
| Status | Backlog |
| Priority | P1 |
| Estimate | 3 points |
| Level | Junior |
| Parent epic | EPIC-02: Persistence and Test Infrastructure |
| Sibling issues | EXP-005, EXP-006 |
| Blocking issues | EXP-006 |
| Blocked issues | EXP-008 |
| Labels | `backend`, `tests`, `auth`, `junior-friendly` |
| Component | User model |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-007-account-state` |
| Suggested PR title | `EXP-007 Add account state helpers and factories` |

## Context

The app represents account state with timestamps, but `fastapi-users` expects
boolean-like properties such as `is_active` and `is_verified`.

## Scope

- Add model properties and setters for account state.
- Add deterministic user factories for tests.
- Add model tests for state transitions.
- Add `__repr__` behavior that avoids sensitive fields.

## Non-Goals

- No HTTP routes.
- No auth manager.
- No password hashing tests.

## Implementation Notes

- `is_active` maps to `deactivated_at is None`.
- `is_deleted` maps to `deleted_at is not None`.
- `is_verified` maps to `email_verified_at is not None`.
- `is_superuser` maps to `superuser_granted_at is not None`.
- Use the shared clock helper so tests can patch current time.

## Acceptance Criteria

- Setting each state property writes or clears the correct timestamp.
- Re-setting a property to its current value is a no-op.
- Factories cover signed-up, verified, logged-in/plain, superuser, and deleted users.
- `repr(user)` does not include `hashed_password`.

## Test Plan

- Run model tests for user state.
- Run factory tests.

## Docs And Team Notes

- README probably does not need a large update unless factory usage becomes a
  common contributor workflow.
- If test factory conventions become repetitive, consider extracting guidance
  into `AGENTS.md`.

## Junior Engineer Guidance

Do not set state timestamps directly in future route handlers. Route code
should use these properties or manager update calls.
