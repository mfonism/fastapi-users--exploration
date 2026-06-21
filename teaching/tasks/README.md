# Task Index

These Markdown files are designed to be copied into GitHub Issues, Linear, or a
similar task-management service.

## Epics

| Epic ID | Epic | Tasks |
|---|---|---|
| E0 | Foundation and tooling | 001-003 |
| E1 | Configuration and database infrastructure | 004-011 |
| E2 | User domain model | 012-015 |
| E3 | Authentication core | 016-022 |
| E4 | Account management | 023-025 |
| E5 | Password and account recovery | 026-029 |
| E6 | Email-change workflow | 030-033 |
| E7 | API polish and docs | 034-035 |

## Dependency Map

```text
001 -> 002, 003, 004
004 -> 005 -> 006 -> 007 -> 008, 009, 012
005 -> 010
002 -> 011
007 -> 012 -> 013, 014 -> 015 -> 016 -> 017 -> 018
018 -> 019 -> 020 -> 021 -> 022
022 -> 023, 024, 025, 027, 032
021 + 024 + 025 -> 026
024 -> 028 -> 029
014 -> 030 -> 031 -> 032 -> 033
018 + 027 + 029 + 033 -> 034
034 -> 035
```

## Suggested Fields For Import

Each task file includes these fields:

- ID
- Title
- Parent epic
- Sibling tasks
- Blocking tasks
- Blocked tasks
- Time estimate
- Difficulty
- Parallelizable
- Suggested labels
- Suggested commit message
- Files
- Description
- Acceptance criteria

## Files

| ID | File | Title |
|---|---|---|
| 001 | [001-scaffold-project.md](001-scaffold-project.md) | Scaffold project |
| 002 | [002-add-fastapi-health-app.md](002-add-fastapi-health-app.md) | Add FastAPI health app |
| 003 | [003-add-lint-format-tooling.md](003-add-lint-format-tooling.md) | Add lint and format tooling |
| 004 | [004-add-environment-model.md](004-add-environment-model.md) | Add environment model |
| 005 | [005-add-settings.md](005-add-settings.md) | Add settings |
| 006 | [006-add-db-session-helpers.md](006-add-db-session-helpers.md) | Add DB session helpers |
| 007 | [007-initialize-alembic.md](007-initialize-alembic.md) | Initialize Alembic |
| 008 | [008-add-db-commands.md](008-add-db-commands.md) | Add DB commands |
| 009 | [009-guard-migrations.md](009-guard-migrations.md) | Guard migrations |
| 010 | [010-add-utilities.md](010-add-utilities.md) | Add utilities |
| 011 | [011-add-app-errors.md](011-add-app-errors.md) | Add app errors |
| 012 | [012-create-user-model.md](012-create-user-model.md) | Create user model |
| 013 | [013-add-user-factories.md](013-add-user-factories.md) | Add user factories |
| 014 | [014-add-account-state-fields.md](014-add-account-state-fields.md) | Add account-state fields |
| 015 | [015-add-user-schemas.md](015-add-user-schemas.md) | Add user schemas |
| 016 | [016-add-user-manager.md](016-add-user-manager.md) | Add user manager |
| 017 | [017-add-redis-auth-backend.md](017-add-redis-auth-backend.md) | Add Redis auth backend |
| 018 | [018-wire-generated-auth-routers.md](018-wire-generated-auth-routers.md) | Wire generated auth routers |
| 019 | [019-test-registration.md](019-test-registration.md) | Test registration |
| 020 | [020-add-verification-flow.md](020-add-verification-flow.md) | Add verification flow |
| 021 | [021-add-login-logout.md](021-add-login-logout.md) | Add login and logout |
| 022 | [022-add-current-user-endpoint.md](022-add-current-user-endpoint.md) | Add current-user endpoint |
| 023 | [023-add-profile-update.md](023-add-profile-update.md) | Add profile update |
| 024 | [024-add-deactivation.md](024-add-deactivation.md) | Add deactivation |
| 025 | [025-add-soft-delete.md](025-add-soft-delete.md) | Add soft delete |
| 026 | [026-add-password-reset.md](026-add-password-reset.md) | Add password reset |
| 027 | [027-add-change-password.md](027-add-change-password.md) | Add change password |
| 028 | [028-add-reactivation-service.md](028-add-reactivation-service.md) | Add reactivation service |
| 029 | [029-add-reactivation-routes.md](029-add-reactivation-routes.md) | Add reactivation routes |
| 030 | [030-add-email-change-model.md](030-add-email-change-model.md) | Add email-change model |
| 031 | [031-add-email-change-request-service.md](031-add-email-change-request-service.md) | Add email-change request service |
| 032 | [032-add-email-change-request-route.md](032-add-email-change-request-route.md) | Add email-change request route |
| 033 | [033-add-email-change-confirmation.md](033-add-email-change-confirmation.md) | Add email-change confirmation |
| 034 | [034-polish-openapi.md](034-polish-openapi.md) | Polish OpenAPI |
| 035 | [035-complete-docs.md](035-complete-docs.md) | Complete docs |

