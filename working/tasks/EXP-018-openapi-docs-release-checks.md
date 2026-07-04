# EXP-018: Finalize OpenAPI Contract, README, And Release Checks

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
| Parent epic | EPIC-07: API Contract and Documentation |
| Sibling issues | None |
| Blocking issues | EXP-002, EXP-014, EXP-015, EXP-017 |
| Blocked issues | None |
| Labels | `backend`, `docs`, `openapi`, `release`, `junior-friendly` |
| Component | Release readiness |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-018-release-readiness` |
| Suggested PR title | `EXP-018 Finalize API contract and docs` |

## Context

The implementation is not ready for handoff until the API contract and local
workflow are documented and verified.

## Scope

- Add OpenAPI contract tests.
- Ensure password fields are write-only.
- Ensure command routes document 204 or 202 correctly.
- Complete README setup and workflow instructions.
- Add API quick checks.
- Document migration workflow and model registry requirement.

## Non-Goals

- No new feature behavior.
- No deployment pipeline unless separately approved.
- No frontend docs.

## Implementation Notes

- Check generated OpenAPI from the app object.
- Empty command responses should not document response content.
- README should work for a new developer starting from a clean checkout.

## Acceptance Criteria

- OpenAPI tests pass.
- README includes prerequisites, `.env` setup, DB bootstrap, migrations, tests,
  linting, and API quick checks.
- Release verification commands are documented.
- No password field is documented as readable.
- All previous feature tests pass.

## Test Plan

- Run `uv run ruff check .`.
- Run `uv run pytest`.
- Run `uv run alembic current`.
- Follow README setup commands from a clean environment if practical.

## Junior Engineer Guidance

Docs are implementation work. If a command in the README does not work, either
fix the command or fix the app so the documented command is true.
