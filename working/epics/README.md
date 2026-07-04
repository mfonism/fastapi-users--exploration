# Epic Index

| Epic ID | Title | Milestone | Primary Outcome |
|---|---|---|---|
| EPIC-01 | Foundation and First App Concepts | Foundation | Packaged app, health endpoint, tooling, simple user shape. |
| EPIC-02 | Persistence and Test Infrastructure | Foundation | Senior-owned DB infrastructure, user persistence, migrations, pytest fixtures. |
| EPIC-03 | Core Authentication | Core Auth | User manager, Redis backend, generated auth routes, registration, verification, login/logout. |
| EPIC-04 | Account Self-Service | Account Management | Current-user routes, profile update, deactivation, soft delete. |
| EPIC-05 | Recovery and Reactivation | Recovery | Password reset/change and account reactivation. |
| EPIC-06 | Email Change Workflow | Email Change | Request and confirm email changes securely. |
| EPIC-07 | API Contract and Documentation | Release | OpenAPI checks and developer workflow docs. |

## Dependency Order

```text
EPIC-01 -> EPIC-02 -> EPIC-03 -> EPIC-04 -> EPIC-05 -> EPIC-06 -> EPIC-07
```

EPIC-02 deliberately starts with a senior-owned infrastructure ticket before
returning to student-friendly model and behavior tickets. Some tasks inside
EPIC-05 and EPIC-06 can run in parallel after EPIC-04 is complete.
