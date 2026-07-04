# EXP-001: Initialize Packaged Project

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Story |
| Status | Backlog |
| Priority | P1 |
| Estimate | 1 point |
| Level | Junior |
| Parent epic | EPIC-01: Foundation and First App Concepts |
| Sibling issues | EXP-002, EXP-003, EXP-004 |
| Blocking issues | None |
| Blocked issues | EXP-002, EXP-003, EXP-004 |
| Labels | `backend`, `project-setup`, `junior-friendly` |
| Component | Project scaffold |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-001-initialize-project` |
| Suggested PR title | `EXP-001 Initialize packaged project` |

## Context

The project should start as a packaged uv application so imports, tests, and
future CLI commands behave like a real Python service.

## Scope

- Initialize a uv-managed packaged application.
- Use a `src/` package layout.
- Add an appropriate `.gitignore`.
- Add a light README with the project name and basic setup intent.

## Non-Goals

- No FastAPI endpoint yet.
- No test suite yet.
- No database setup.
- No auth setup.
- No environment settings.

## Implementation Notes

- Follow uv's packaged application guidance.
- The importable application package should be named `explore`.
- Keep the README small; later tasks will expand it as the app gains behavior.

## Acceptance Criteria

- `uv sync` succeeds.
- The package can be imported with `uv run python -c "import explore"`.
- Local caches, virtual environments, build artifacts, and real env files are
  ignored by git.
- No local secrets are committed.

## Test Plan

- Run `uv sync`.
- Run a package import smoke check.

## Docs And Team Notes

- README should mention how to install/sync dependencies.
- No `AGENTS.md` or skill extraction is expected yet.

## Junior Engineer Guidance

This task is only about making the project real as a Python package. Avoid
adding app behavior until the health endpoint ticket.
