# EXP-009: Configure Redis Auth Backend And Generated Auth Routers

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
| Sibling issues | EXP-008, EXP-010, EXP-011 |
| Blocking issues | EXP-008 |
| Blocked issues | EXP-010 |
| Labels | `backend`, `auth`, `redis`, `api` |
| Component | Auth routing |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-009-redis-auth-routes` |
| Suggested PR title | `EXP-009 Configure Redis backend and auth routers` |

## Context

The service needs bearer-token auth with token revocation and generated
registration, verification, and password-reset routes.

## Scope

- Add Redis auth strategy.
- Add bearer transport.
- Instantiate `FastAPIUsers`.
- Include generated register, verify, and reset-password routers.
- Mount the auth router in the main app.

## Non-Goals

- No custom current-user routes.
- No custom password-change route.
- No reactivation or email-change routes.

## Implementation Notes

- Use settings for Redis URL and key prefix.
- Token lifetime should match the target implementation.
- The router module should be the single place that composes auth subrouters.

## Acceptance Criteria

- Auth backend is named `redis`.
- Redis key prefix changes in test environment.
- Generated routes appear in OpenAPI.
- Main app includes the auth router.
- No endpoint exposes raw password fields.

## Test Plan

- Inspect OpenAPI route list.
- Run a route import smoke test.
- Downstream tickets add full endpoint tests.

## Junior Engineer Guidance

Do not copy generated route code from the library. Use the library methods and
configure them with our schemas, manager, and backend.
