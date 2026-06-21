# Parallelization Plan

Do not parallelize the earliest infrastructure tasks. Students need the same
project shape, dependencies, settings, database layer, user model, auth manager,
Redis backend, login flow, and `/users/me` endpoint before independent work is
productive.

The safe split point is after task 22: **Add current-user endpoint**.

## Parallel Branches

| Branch | Tasks | Best For | Notes |
|---|---|---|---|
| A: Profile and account state | 23, 24, 25 | Beginner pairs | Mostly schemas, route handlers, and state transitions. |
| B: Password workflows | 26, 27 | Early intermediate pairs | Shows both generated router customization and custom service routes. |
| C: Reactivation | 28, 29 | Stronger students | Includes JWT claims, stale-token checks, and non-enumeration behavior. |
| D: Email changes | 30, 31, 32, 33 | Stronger group or two pairs | Largest branch; split model/service from route/confirmation work. |
| E: OpenAPI and docs | 34, 35 | Documentation-focused pair | Can run late while feature branches finish. |

## Merge Order

Recommended merge order:

1. Branch A
2. Branch B
3. Branch C
4. Branch D
5. Branch E

This order reduces conflicts because reactivation depends on deactivation and
email-change confirmation depends on soft-delete/current-session behavior.

## Expected Conflict Hotspots

| File | Why Conflicts Happen | Mitigation |
|---|---|---|
| `src/explore/auth/routes.py` | Multiple branches include new routers. | Reserve a final router-wiring slot or merge often. |
| `src/explore/auth/users/models.py` | Account-state and email-change work may touch user state expectations. | Complete core model fields before branching. |
| `src/explore/auth/users/manager.py` | Password reset, deleted-user checks, login hooks, and verification hooks meet here. | Assign one branch owner for manager changes. |
| `alembic/versions/*` | Parallel migrations create independent revision heads. | Rebase migrations before merge or have one migration captain. |
| `tests/conftest.py` | Auth fixtures may need updates for multiple branches. | Keep shared fixtures stable after task 22. |

## Suggested Group Assignments

For a classroom:

- group 1: profile update and deactivation
- group 2: soft delete and current-token logout
- group 3: password change
- group 4: password reset edge cases
- group 5: reactivation service
- group 6: email-change model and helpers
- group 7: email-change routes and confirmation
- group 8: OpenAPI and docs

For a shorter conference tutorial:

- teach tasks 1-22 together
- demo branch A live
- assign branch B or D as optional lab work
- discuss branch C as a security-focused stretch

