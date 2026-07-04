# EXP-010: Build Registration And Verification Flows

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Story |
| Status | Backlog |
| Priority | P1 |
| Estimate | 5 points |
| Level | Intermediate |
| Parent epic | EPIC-03: Core Authentication |
| Sibling issues | EXP-008, EXP-009, EXP-011 |
| Blocking issues | EXP-009 |
| Blocked issues | EXP-011 |
| Labels | `backend`, `auth`, `tests`, `security` |
| Component | Registration |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-010-registration-verification` |
| Suggested PR title | `EXP-010 Cover registration and verification flows` |

## Context

Registration and verification are the first complete auth flows. They need
database writes, password hashing, schema validation, token handling, and
notification hooks.

## Scope

- Add endpoint tests for registration.
- Add endpoint tests for verification token request.
- Add endpoint tests for verification confirmation.
- Ensure deleted users are hidden or rejected correctly.
- Ensure already verified users are handled idempotently.

## Non-Goals

- No login/logout behavior.
- No real email delivery.

## Implementation Notes

- Patch notification functions in tests.
- Assert password hashes are not equal to submitted passwords.
- Assert response payloads hide internal fields.
- Use factories for existing-user setup.

## Acceptance Criteria

- Registration creates a user with normalized email.
- Duplicate normalized emails are rejected.
- Invalid payloads return 422.
- Verification request calls the notification placeholder.
- Valid verification token marks user verified.
- Expired, invalid, and deleted-user verification cases are covered.

## Test Plan

- Run registration tests.
- Run verification request and verification confirmation tests.
- Run all auth model tests if touched.

## Junior Engineer Guidance

Write the tests as user stories: "given this account state, when this request
happens, then this response and DB change should occur."
