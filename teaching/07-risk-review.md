# Risk Review

Some final-codebase pieces are useful in a real project but too complex to
teach too early. Use this review to decide what to simplify, defer, or provide
as starter code.

| Area | Risk For Beginners | Recommendation |
|---|---|---|
| `fastapi-users` generated routers | Students may feel behavior appears by magic. | Teach one generated route first, then show the manager/schema/backend hooks that customize it. |
| Generic types in `FastAPIUsers[User, uuid.UUID]` and `BaseUserManager[User, uuid.UUID]` | Type syntax may distract from auth flow. | Explain as "the library needs to know our user type and ID type"; defer deeper generics discussion. |
| Async SQLAlchemy sessions | Async context managers, dependency yields, and session lifetimes are several concepts at once. | Provide the session helper early and revisit it during tests. |
| Transactional test fixture with nested savepoints | Correct but advanced. | Provide as starter code in a workshop, then explain why tests stay isolated. |
| PostgreSQL role/database bootstrap | Operational detail can consume class time. | Hide behind `uv run db-bootstrap`; only teach migrations directly. |
| PostgreSQL version check and `uuidv7()` server defaults | Environment-specific and can fail on student machines. | Use a provided Docker command or replace with simpler UUID defaults in a beginner-only variant. |
| Redis token strategy | Requires another service and auth vocabulary. | Draw the login/logout flow. Students do not need to inspect Redis internals. |
| Password hashing and invalid login timing | Security-sensitive and non-obvious. | Explain at a high level; avoid implementing hashing manually. |
| Soft deletion mixed with `fastapi-users` active checks | Deleted, inactive, and unverified states can blur together. | Use a state table and write model tests before routes. |
| Reactivation stale-token validation | JWT claims plus state comparison is subtle. | Make this a stretch branch for stronger students. |
| Email-change token hashing and race handling | Requires token security, expiry, cancellation, and DB integrity handling. | Teach model helpers first; add race-safe `IntegrityError` handling last. |
| Alembic parallel migrations | Student branches can create multiple heads. | Assign one migration captain or merge migration branches sequentially. |
| OpenAPI polish for empty responses | Looks minor but requires route metadata details. | Teach after features work, as documentation polish. |

## Simplified Workshop Variant

For a one-day beginner workshop, consider stopping at:

1. health endpoint
2. settings
3. DB session
4. user model
5. registration
6. verification
7. login/logout
8. `/users/me`
9. profile update
10. change password

Defer:

- DB bootstrap internals
- soft delete
- reactivation
- email changes
- migration guard script
- PostgreSQL trigger for `updated_at`

## Instructor Starter Code Candidates

Provide these files up front if time is tight:

- `src/explore/db/config.py`
- `src/explore/db/bootstrap.py`
- `src/explore/db/migrate.py`
- `tests/conftest.py`
- `.pre-commit-config.yaml`
- `scripts/check_empty_migrations.py`

Then have students implement feature modules, tests, and migrations.

